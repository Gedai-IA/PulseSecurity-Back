from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from app.domain.entities.comment import Comment, AnalyzedComment
from app.domain.value_objects.sentiment import Sentiment
from app.domain.value_objects.emotion import Emotion
from app.domain.value_objects.topic import Topic


@dataclass
class Publication:
    """Entidade de publicação."""
    publicacao_n: int
    url: str
    description: str
    date: datetime
    views: Optional[str] = None
    likes: Optional[str] = None
    comments_count: int = 0
    shares: Optional[str] = None
    bookmarks: Optional[str] = None
    music_title: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    
    def get_all_text_content(self) -> List[str]:
        """Retorna todo o conteúdo textual da publicação."""
        texts = [self.description]
        for comment in self.comments:
            texts.append(comment.text)
            for reply in comment.replies:
                texts.append(reply.text)
        return texts


@dataclass
class AnalyzedPublication:
    """Publicação com análises agregadas."""
    publication: Publication
    main_sentiment: Sentiment
    main_emotion: Emotion
    main_topic: Topic
    analyzed_comments: List[AnalyzedComment] = field(default_factory=list)
    analyzed_at: Optional[datetime] = None

