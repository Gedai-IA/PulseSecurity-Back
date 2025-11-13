from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.publication import Publication
from app.infrastructure.database.repositories.publication_repository import PublicationRepository
from app.infrastructure.database.models import PublicationModel
from app.domain.entities.comment import Comment, Reply


class PublicationService:
    """Serviço de gerenciamento de publicações."""
    
    def __init__(self, session: AsyncSession):
        self.repository = PublicationRepository(session)
    
    async def create_publication(self, publication: Publication) -> PublicationModel:
        """Cria uma nova publicação."""
        # Verifica se já existe
        existing = await self.repository.get_by_publicacao_n(publication.publicacao_n)
        if existing:
            return existing
        
        return await self.repository.create(publication)
    
    async def get_publication(self, publication_id: int) -> Optional[PublicationModel]:
        """Obtém uma publicação por ID."""
        return await self.repository.get_by_id(publication_id)
    
    async def list_publications(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[PublicationModel]:
        """Lista publicações com filtros."""
        return await self.repository.list(
            start_date=start_date,
            end_date=end_date,
            tags=tags,
            limit=limit,
            offset=offset,
        )
    
    async def search_publications(self, query: str, limit: int = 100) -> List[PublicationModel]:
        """Busca publicações por texto."""
        return await self.repository.search(query, limit=limit)
    
    async def count_publications(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> int:
        """Conta publicações com filtros."""
        return await self.repository.count(
            start_date=start_date,
            end_date=end_date,
            tags=tags,
        )

