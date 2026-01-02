from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.moderation import router as moderation_router



app = FastAPI(title=settings.APP_NAME)

app.include_router(
    moderation_router,
    prefix="/api/v1",
    tags=["Moderation"]
)

@app.get("/")
def root():
    return {"status": "Ok", "Service": settings.APP_NAME}

