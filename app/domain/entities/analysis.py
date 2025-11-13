from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from app.domain.value_objects.sentiment import Sentiment
from app.domain.value_objects.emotion import Emotion
from app.domain.value_objects.topic import Topic


@dataclass
class DashboardStats:
    """Estatísticas agregadas para o dashboard."""
    total_publications: int
    total_comments: int
    threat_count: int
    negative_sentiment_percent: float
    sentiment_distribution: Dict[Sentiment, int]
    emotion_distribution: Dict[Emotion, int]
    topic_distribution: Dict[Topic, int]
    date_range: Optional[tuple[datetime, datetime]] = None

