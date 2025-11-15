from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.application.services.publication_service import PublicationService
from app.api.v1.schemas.publication_schemas import (
    PublicationCreateSchema,
    PublicationResponseSchema,
    PublicationListResponseSchema,
)

router = APIRouter()


@router.post("/publications", response_model=PublicationResponseSchema, status_code=201)
async def create_publication(
    publication: PublicationCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Cria uma nova publicação."""
    service = PublicationService(db)
    
    from app.domain.entities.publication import Publication
    from app.domain.entities.comment import Comment, Reply
    
    # Converte schema para entidade
    comments = [
        Comment(
            username=c.username,
            text=c.text,
            likes=c.likes,
            replies=[Reply(username=r.username, text=r.text, likes=r.likes) for r in c.replies]
        )
        for c in publication.comments
    ]
    
    pub_entity = Publication(
        publicacao_n=publication.publicacao_n,
        url=str(publication.url),
        description=publication.description,
        date=publication.date,
        views=publication.views,
        likes=publication.likes,
        comments_count=publication.comments_count,
        shares=publication.shares,
        bookmarks=publication.bookmarks,
        music_title=publication.music_title,
        tags=publication.tags,
        comments=comments,
    )
    
    result = await service.create_publication(pub_entity)
    return result


@router.get("/publications", response_model=PublicationListResponseSchema)
async def list_publications(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    tags: Optional[List[str]] = Query(None),
    limit: int = Query(100, ge=1, le=10000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """Lista publicações com filtros."""
    service = PublicationService(db)
    
    items = await service.list_publications(
        start_date=start_date,
        end_date=end_date,
        tags=tags,
        limit=limit,
        offset=offset,
    )
    
    total = await service.count_publications(
        start_date=start_date,
        end_date=end_date,
        tags=tags,
    )
    
    return PublicationListResponseSchema(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/publications/{publication_id}", response_model=PublicationResponseSchema)
async def get_publication(
    publication_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Obtém uma publicação por ID."""
    service = PublicationService(db)
    publication = await service.get_publication(publication_id)
    
    if not publication:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(f"Publicação {publication_id} não encontrada")
    
    return publication


@router.get("/publications/search", response_model=PublicationListResponseSchema)
async def search_publications(
    q: str = Query(..., min_length=1),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Busca publicações por texto."""
    service = PublicationService(db)
    items = await service.search_publications(q, limit=limit)
    
    return PublicationListResponseSchema(
        items=items,
        total=len(items),
        limit=limit,
        offset=0,
    )

