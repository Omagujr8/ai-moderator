from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.content import Content
from app.ai.nlp.toxicity import analyze_text
from app.ai.pipelines.decision_engine import decide_text
from app.ai.vision.nsfw import analyze_image
from app.models.moderation_result import ModerationResult
#from app.services.webhook_service import send_webhook
from app.core.logging import logger
from app.ai.nlp.toxicity_multilingual import analyze_text_multilingual
from app.ai.nlp.language_detect import detect_language
from app.services.video_moderation_service import moderate_video
from app.services.pii_service import mask_email, hash_username
import time
from app.core.metrics import (
    moderation_requests_total,
    moderation_decisions_total,
    moderation_duration_seconds
)


def save_results(db, content_id, results, decision, model_version):
    for r in results:
        db.add(
            ModerationResult(
                content_id=content_id,
                category=r["label"],
                score=r["score"],
                decision=decision,
                model_version=model_version
            )
        )
def run_moderation(content_id:int):
    db: Session = SessionLocal()
    content = db.query(Content).get(content_id)
    start_time = time.time()
    moderation_requests_total.inc()

    if not content:
        db.close()
        return
    decision = "approved"

    if content.text:
        clean_text = mask_email(content.text)
        lang = detect_language(content.text)

        try:
            if lang == "en":
                text_results = analyze_text(content.text)
            else:
                text_results = analyze_text_multilingual(content.text)

            decision, model_version = decide_text(text_results)

            save_results(
                db=db,
                content_id=content.id,
                results=text_results,
                decision=decision,
                model_version=model_version
            )
        except Exception as e:
            logger.error(f"AI text model failed: {e}")
            decision = "approved"  # safe default
            model_version = "error"

    if content.image_url:
        try:
            image_results = analyze_image(content.image_url)
            if image_results:
                decision = "blocked"
        except Exception as e:
            logger.error(f"AI image model failed: {e}")
            decision = "approved"

    if content.video_url:
        try:
            safe = moderate_video(content.video_url)
            if not safe:
                decision = "blocked"
        except Exception as e:
            logger.error(f"Video moderation failed: {e}")
            decision = "approved"

    moderation_decisions_total.labels(decision=decision).inc()
    content.username_hashed = hash_username(content.username)

    content.status = decision
    db.commit()

    logger.info(
        f"Content {content.id} | Decision: {decision} | Source: {content.source_app}"
    )
    logger.info(
        f"Moderation took {time.time() - start_time:.2f}s"
    )

    payload = {
        "content_id": content_id,
        "decision": decision,
        "status": content.status,
        "model_version": model_version
    }

    #send_webhook("https://client-app/webhook",payload)

    db.close()