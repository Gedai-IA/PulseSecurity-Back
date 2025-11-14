from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.application.services.analysis_service import AnalysisService
from app.api.v1.schemas.dashboard_schemas import DashboardStatsResponseSchema

router = APIRouter()


@router.get("/dashboard/stats", response_model=DashboardStatsResponseSchema)
async def get_dashboard_stats(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tags: Optional[list[str]] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Obtém estatísticas agregadas para o dashboard."""
    service = AnalysisService(db)
    stats = await service.get_dashboard_stats(
        start_date=start_date,
        end_date=end_date,
        tags=tags,
    )
    
    # Converte enums para strings para serialização JSON
    return DashboardStatsResponseSchema(
        total_publications=stats.total_publications,
        total_comments=stats.total_comments,
        threat_count=stats.threat_count,
        negative_sentiment_percent=stats.negative_sentiment_percent,
        sentiment_distribution={k.value: v for k, v in stats.sentiment_distribution.items()},
        emotion_distribution={k.value: v for k, v in stats.emotion_distribution.items()},
        topic_distribution={k.value: v for k, v in stats.topic_distribution.items()},
        date_range=stats.date_range,
    )

