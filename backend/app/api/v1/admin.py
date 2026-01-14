from fastapi import APIRouter, Depends
from app.core.security import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
def list_users(user=Depends(require_role("admin"))):
    return {"users": []}
