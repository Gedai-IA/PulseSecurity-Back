from fastapi import APIRouter

router = APIRouter()


@router.post("/auth/login")
async def login():
    """Endpoint de login (placeholder)."""
    return {"message": "Login endpoint - to be implemented"}


@router.post("/auth/register")
async def register():
    """Endpoint de registro (placeholder)."""
    return {"message": "Register endpoint - to be implemented"}

