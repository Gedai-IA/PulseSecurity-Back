from pydantic import BaseModel
from typing import Dict, Optional, List
from datetime import datetime


class DashboardStatsResponseSchema(BaseModel):
    total_publications: int
    total_comments: int
    threat_count: int
    negative_sentiment_percent: float
    sentiment_distribution: Dict[str, int]
    emotion_distribution: Dict[str, int]
    topic_distribution: Dict[str, int]
    date_range: Optional[List[datetime]] = None


class FilterParamsSchema(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tags: Optional[list[str]] = None
    limit: int = 100
    offset: int = 0

