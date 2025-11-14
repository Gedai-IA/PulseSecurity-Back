from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List

from app.infrastructure.database.session import Base


class PublicationModel(Base):
    """Model SQLAlchemy para Publicação."""
    __tablename__ = "publications"
    
    id = Column(Integer, primary_key=True, index=True)
    publicacao_n = Column(Integer, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    views = Column(String, nullable=True)
    likes = Column(String, nullable=True)
    comments_count = Column(Integer, default=0)
    shares = Column(String, nullable=True)
    bookmarks = Column(String, nullable=True)
    music_title = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = relationship("CommentModel", back_populates="publication", cascade="all, delete-orphan")
    analyses = relationship("PublicationAnalysisModel", back_populates="publication", uselist=False)


class CommentModel(Base):
    """Model SQLAlchemy para Comentário."""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), nullable=False)
    username = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    publication = relationship("PublicationModel", back_populates="comments")
    replies = relationship("ReplyModel", back_populates="comment", cascade="all, delete-orphan")
    analyses = relationship("CommentAnalysisModel", back_populates="comment", uselist=False)


class ReplyModel(Base):
    """Model SQLAlchemy para Resposta."""
    __tablename__ = "replies"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    username = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    comment = relationship("CommentModel", back_populates="replies")


class PublicationAnalysisModel(Base):
    """Model SQLAlchemy para Análise de Publicação."""
    __tablename__ = "publication_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), unique=True, nullable=False)
    main_sentiment = Column(String, nullable=False)
    main_emotion = Column(String, nullable=False)
    main_topic = Column(String, nullable=False)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    publication = relationship("PublicationModel", back_populates="analyses")


class CommentAnalysisModel(Base):
    """Model SQLAlchemy para Análise de Comentário."""
    __tablename__ = "comment_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), unique=True, nullable=False)
    sentiment = Column(String, nullable=False)
    emotion = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    comment = relationship("CommentModel", back_populates="analyses")

