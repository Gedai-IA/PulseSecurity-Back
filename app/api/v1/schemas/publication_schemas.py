from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class ReplySchema(BaseModel):
    username: str
    text: str
    likes: int = 0


class CommentSchema(BaseModel):
    username: str
    text: str
    likes: int = 0
    replies: List[ReplySchema] = []


class PublicationCreateSchema(BaseModel):
    publicacao_n: int
    url: HttpUrl
    description: str
    date: datetime
    views: Optional[str] = None
    likes: Optional[str] = None
    comments_count: int = 0
    shares: Optional[str] = None
    bookmarks: Optional[str] = None
    music_title: Optional[str] = None
    tags: List[str] = []
    comments: List[CommentSchema] = []


class PublicationResponseSchema(BaseModel):
    id: int
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
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PublicationListResponseSchema(BaseModel):
    items: List[PublicationResponseSchema]
    total: int
    limit: int
    offset: int

