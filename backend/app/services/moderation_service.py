# from app.core.celery import celery_app
#from app.services.moderation_service import run_moderation


# @celery_app.task
# def run_moderation(content_id: int):
#     print(f"[MODERATION] Running moderation for content ID: {content_id}")


from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.content import Content
from app.ai.nlp.toxicity import analyze_text
from app.ai.pipelines.decision_engine import decide_text
from app.ai.vision.nsfw import analyze_image
from app.models.moderation_result import ModerationResult


def save_results(db, content_id, results, decision):
    for r in results:
        db.add(
            ModerationResult(
                content_id=content_id,
                category=r["label"],
                score=r["score"],
                decision=decision,
                model_version="v1-toxic-bert"
            )
        )
def run_moderation(content_id:int):
    db: Session = SessionLocal()
    content = db.query(Content).get(content_id)

    if not content:
        db.close()
        return
    decision = "approved"

    if content.text:
        text_results = analyze_text(content.text)
        decision = decide_text(text_results)

    if content.image_url:
        image_results = analyze_image(content.image_url)
        if image_results:
            decision = "blocked"

    content.status = decision
    db.commit()
    db.close()

