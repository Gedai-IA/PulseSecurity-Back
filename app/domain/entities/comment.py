from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from app.domain.value_objects.sentiment import Sentiment
from app.domain.value_objects.emotion import Emotion
from app.domain.value_objects.topic import Topic


@dataclass
class Reply:
    """Entidade de resposta a comentário."""
    username: str
    text: str
    likes: int = 0


@dataclass
class Comment:
    """Entidade de comentário."""
    username: str
    text: str
    likes: int = 0
    replies: List[Reply] = None
    
    def __post_init__(self):
        if self.replies is None:
            self.replies = []


@dataclass
class AnalyzedComment:
    """Comentário com análise de NLP."""
    comment: Comment
    sentiment: Sentiment
    emotion: Emotion
    topic: Topic
    analyzed_at: datetime

