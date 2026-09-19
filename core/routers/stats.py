from fastapi import APIRouter

from core.stats import get_stats

router = APIRouter()


@router.get("/stats")
def stats():
    return get_stats()
