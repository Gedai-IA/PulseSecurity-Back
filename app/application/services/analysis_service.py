from typing import List, Dict, Optional
from datetime import datetime
from collections import Counter
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.analysis import DashboardStats
from app.domain.entities.publication import Publication
from app.domain.value_objects.sentiment import Sentiment
from app.domain.value_objects.emotion import Emotion
from app.domain.value_objects.topic import Topic
from app.application.services.publication_service import PublicationService
from app.application.services.nlp_service import NLPService


class AnalysisService:
    """Serviço de análise e agregação de dados."""
    
    def __init__(self, session: AsyncSession):
        self.publication_service = PublicationService(session)
        self.nlp_service = NLPService()
    
    async def get_dashboard_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> DashboardStats:
        """Gera estatísticas agregadas para o dashboard."""
        publications = await self.publication_service.list_publications(
            start_date=start_date,
            end_date=end_date,
            tags=tags,
            limit=10000,  # Limite alto para análise completa
        )
        
        if not publications:
            return DashboardStats(
                total_publications=0,
                total_comments=0,
                threat_count=0,
                negative_sentiment_percent=0.0,
                sentiment_distribution={},
                emotion_distribution={},
                topic_distribution={},
                date_range=(start_date, end_date) if start_date and end_date else None,
            )
        
        # Processa todas as publicações
        all_sentiments = []
        all_emotions = []
        all_topics = []
        total_comments = 0
        threat_count = 0
        
        for pub_model in publications:
            # Converte para entidade de domínio
            publication = self._model_to_entity(pub_model)
            
            # Analisa publicação
            analyzed = self.nlp_service.analyze_publication(publication)
            
            # Coleta dados
            all_sentiments.append(analyzed.main_sentiment)
            all_emotions.append(analyzed.main_emotion)
            all_topics.append(analyzed.main_topic)
            
            total_comments += len(publication.comments)
            for comment in publication.comments:
                total_comments += len(comment.replies)
            
            # Conta ameaças
            if analyzed.main_topic == Topic.AMEACAS_E_RISCOS:
                threat_count += 1
            
            # Conta sentimento negativo
            for analyzed_comment in analyzed.analyzed_comments:
                all_sentiments.append(analyzed_comment.sentiment)
                all_emotions.append(analyzed_comment.emotion)
                all_topics.append(analyzed_comment.topic)
                
                if analyzed_comment.topic == Topic.AMEACAS_E_RISCOS:
                    threat_count += 1
        
        # Calcula distribuições
        sentiment_counts = Counter(all_sentiments)
        emotion_counts = Counter(all_emotions)
        topic_counts = Counter(all_topics)
        
        # Calcula percentual de sentimento negativo
        total_sentiments = len(all_sentiments)
        negative_count = sentiment_counts.get(Sentiment.NEGATIVO, 0)
        negative_percent = (negative_count / total_sentiments * 100) if total_sentiments > 0 else 0.0
        
        # Determina range de datas
        dates = [pub.date for pub in publications if pub.date]
        date_range = (min(dates), max(dates)) if dates else None
        
        return DashboardStats(
            total_publications=len(publications),
            total_comments=total_comments,
            threat_count=threat_count,
            negative_sentiment_percent=negative_percent,
            sentiment_distribution=dict(sentiment_counts),
            emotion_distribution=dict(emotion_counts),
            topic_distribution=dict(topic_counts),
            date_range=date_range,
        )
    
    def _model_to_entity(self, pub_model) -> Publication:
        """Converte model SQLAlchemy para entidade de domínio."""
        comments = []
        for comment_model in pub_model.comments:
            replies = [
                Reply(
                    username=reply_model.username,
                    text=reply_model.text,
                    likes=reply_model.likes or 0,
                )
                for reply_model in comment_model.replies
            ]
            
            comments.append(Comment(
                username=comment_model.username,
                text=comment_model.text,
                likes=comment_model.likes or 0,
                replies=replies,
            ))
        
        return Publication(
            publicacao_n=pub_model.publicacao_n,
            url=pub_model.url,
            description=pub_model.description,
            date=pub_model.date,
            views=pub_model.views,
            likes=pub_model.likes,
            comments_count=pub_model.comments_count or 0,
            shares=pub_model.shares,
            bookmarks=pub_model.bookmarks,
            music_title=pub_model.music_title,
            tags=pub_model.tags or [],
            comments=comments,
        )

