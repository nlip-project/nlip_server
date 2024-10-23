from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.get("/health/live")
async def liveness_check():
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness_check():
    return {"status": "ready"}
