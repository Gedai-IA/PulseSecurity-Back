from typing import List
from datetime import datetime

from app.domain.entities.comment import Comment, AnalyzedComment
from app.domain.entities.publication import Publication, AnalyzedPublication
from app.infrastructure.nlp.sentiment_analyzer import SentimentAnalyzer
from app.infrastructure.nlp.emotion_classifier import EmotionClassifier
from app.infrastructure.nlp.topic_classifier import TopicClassifier
from app.domain.value_objects.sentiment import Sentiment
from app.domain.value_objects.emotion import Emotion
from app.domain.value_objects.topic import Topic


class NLPService:
    """Serviço de processamento de linguagem natural."""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.emotion_classifier = EmotionClassifier()
        self.topic_classifier = TopicClassifier()
    
    def analyze_comment(self, comment: Comment) -> AnalyzedComment:
        """Analisa um comentário."""
        sentiment = self.sentiment_analyzer.analyze(comment.text)
        emotion = self.emotion_classifier.classify(comment.text)
        topic = self.topic_classifier.classify(comment.text)
        
        return AnalyzedComment(
            comment=comment,
            sentiment=sentiment,
            emotion=emotion,
            topic=topic,
            analyzed_at=datetime.utcnow()
        )
    
    def analyze_publication(self, publication: Publication) -> AnalyzedPublication:
        """Analisa uma publicação completa."""
        analyzed_comments = []
        
        # Analisa descrição
        desc_sentiment = self.sentiment_analyzer.analyze(publication.description)
        desc_emotion = self.emotion_classifier.classify(publication.description)
        desc_topic = self.topic_classifier.classify(publication.description)
        
        # Analisa comentários
        for comment in publication.comments:
            analyzed_comment = self.analyze_comment(comment)
            analyzed_comments.append(analyzed_comment)
            
            # Analisa respostas
            for reply in comment.replies:
                reply_comment = Comment(
                    username=reply.username,
                    text=reply.text,
                    likes=reply.likes
                )
                analyzed_reply = self.analyze_comment(reply_comment)
                analyzed_comments.append(analyzed_reply)
        
        # Determina sentimento/emoção/tópico principal
        sentiments = [desc_sentiment] + [ac.sentiment for ac in analyzed_comments]
        emotions = [desc_emotion] + [ac.emotion for ac in analyzed_comments]
        topics = [desc_topic] + [ac.topic for ac in analyzed_comments]
        
        # Conta ocorrências
        sentiment_counts = {}
        for s in sentiments:
            sentiment_counts[s] = sentiment_counts.get(s, 0) + 1
        
        emotion_counts = {}
        for e in emotions:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
        
        topic_counts = {}
        for t in topics:
            topic_counts[t] = topic_counts.get(t, 0) + 1
        
        # Determina o mais frequente (desempate: Negativo > Positivo > Neutro)
        main_sentiment = max(sentiment_counts.items(), key=lambda x: (x[1], x[0] != Sentiment.NEUTRO))[0]
        main_emotion = max(emotion_counts.items(), key=lambda x: (x[1], x[0] != Emotion.GERAL))[0]
        main_topic = max(topic_counts.items(), key=lambda x: (x[1], x[0] != Topic.GERAL))[0]
        
        return AnalyzedPublication(
            publication=publication,
            main_sentiment=main_sentiment,
            main_emotion=main_emotion,
            main_topic=main_topic,
            analyzed_comments=analyzed_comments,
            analyzed_at=datetime.utcnow()
        )

