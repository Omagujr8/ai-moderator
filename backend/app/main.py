from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.moderation import router as moderation_router
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

app = FastAPI(title=settings.APP_NAME)

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
    tags=["Moderation"]
)

@app.get("/")
def root():
    return {"status": "Ok", "Service": settings.APP_NAME}

