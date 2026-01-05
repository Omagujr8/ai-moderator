from fastapi import Depends, HTTPException, status
from app.core.security import verify_api_key

def require_role(required_role: str):
    def checker(user=Depends(verify_api_key)):
        if user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return user
    return checker
