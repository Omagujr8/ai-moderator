from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.moderation import router as moderation_router
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.logging import logger

app = FastAPI(title=settings.APP_NAME)

Instrumentator().instrument(app).expose(app)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )
)

app.include_router(
    moderation_router,
    prefix="/api/v1",
)

# Scheduler disabled on Windows (APScheduler has issues with billiard on Windows)
# Enable in production with proper deployment setup
# from apscheduler.schedulers.background import BackgroundScheduler
# from app.services.cleanup_service import cleanup_old_content
# scheduler = BackgroundScheduler()
# scheduler.add_job(cleanup_old_content, "interval", days=1)
# scheduler.start()

@app.get("/")
def root():
    return {"status": "Ok", "Service": settings.APP_NAME}

@app.get("/health")
def health():
    return {
        "api": "ok",
        "env": settings.ENV
    }

@app.on_event("shutdown")
def shutdown():
    logger.info("Shutting down cleanly")