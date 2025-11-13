from fastapi import APIRouter

router = APIRouter()


@router.get("/analysis/health")
async def analysis_health():
    """Health check do serviço de análise."""
    return {"status": "healthy", "service": "analysis"}

