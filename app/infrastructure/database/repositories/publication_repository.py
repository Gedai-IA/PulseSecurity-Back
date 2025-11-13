from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, String as SQLString
from sqlalchemy.orm import selectinload

from app.domain.entities.publication import Publication
from app.domain.entities.comment import Comment, Reply
from app.infrastructure.database.models import (
    PublicationModel,
    CommentModel,
    ReplyModel
)


class PublicationRepository:
    """Repository para operações com publicações."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, publication: Publication) -> PublicationModel:
        """Cria uma nova publicação."""
        db_publication = PublicationModel(
            publicacao_n=publication.publicacao_n,
            url=publication.url,
            description=publication.description,
            date=publication.date,
            views=publication.views,
            likes=publication.likes,
            comments_count=publication.comments_count,
            shares=publication.shares,
            bookmarks=publication.bookmarks,
            music_title=publication.music_title,
            tags=publication.tags,
        )
        
        # Adiciona comentários
        for comment in publication.comments:
            db_comment = CommentModel(
                username=comment.username,
                text=comment.text,
                likes=comment.likes,
            )
            # Adiciona respostas
            for reply in comment.replies:
                db_reply = ReplyModel(
                    username=reply.username,
                    text=reply.text,
                    likes=reply.likes,
                )
                db_comment.replies.append(db_reply)
            
            db_publication.comments.append(db_comment)
        
        self.session.add(db_publication)
        await self.session.commit()
        await self.session.refresh(db_publication)
        return db_publication
    
    async def get_by_id(self, publication_id: int) -> Optional[PublicationModel]:
        """Busca publicação por ID."""
        stmt = select(PublicationModel).where(
            PublicationModel.id == publication_id
        ).options(
            selectinload(PublicationModel.comments).selectinload(CommentModel.replies)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_publicacao_n(self, publicacao_n: int) -> Optional[PublicationModel]:
        """Busca publicação por número de publicação."""
        stmt = select(PublicationModel).where(
            PublicationModel.publicacao_n == publicacao_n
        ).options(
            selectinload(PublicationModel.comments).selectinload(CommentModel.replies)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[PublicationModel]:
        """Lista publicações com filtros."""
        stmt = select(PublicationModel).options(
            selectinload(PublicationModel.comments).selectinload(CommentModel.replies)
        )
        
        conditions = []
        if start_date:
            conditions.append(PublicationModel.date >= start_date)
        if end_date:
            conditions.append(PublicationModel.date <= end_date)
        if tags:
            conditions.append(PublicationModel.tags.contains(tags))
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        stmt = stmt.order_by(PublicationModel.date.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def search(self, query: str, limit: int = 100) -> List[PublicationModel]:
        """Busca publicações por texto."""
        stmt = select(PublicationModel).where(
            or_(
                PublicationModel.description.ilike(f"%{query}%"),
                PublicationModel.publicacao_n.cast(SQLString).ilike(f"%{query}%")
            )
        ).options(
            selectinload(PublicationModel.comments).selectinload(CommentModel.replies)
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def count(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> int:
        """Conta publicações com filtros."""
        from sqlalchemy import func
        
        stmt = select(func.count(PublicationModel.id))
        
        conditions = []
        if start_date:
            conditions.append(PublicationModel.date >= start_date)
        if end_date:
            conditions.append(PublicationModel.date <= end_date)
        if tags:
            conditions.append(PublicationModel.tags.contains(tags))
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        result = await self.session.execute(stmt)
        return result.scalar() or 0

