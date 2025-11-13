"""
Script para importar dados JSON para o banco de dados.
Uso: uv run python scripts/import_json.py <caminho_do_json>
"""
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import AsyncSessionLocal
from app.application.services.publication_service import PublicationService
from app.domain.entities.publication import Publication
from app.domain.entities.comment import Comment, Reply


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime."""
    try:
        # Formato: "2-1" (dia-mês)
        if "-" in date_str and len(date_str.split("-")) == 2:
            day, month = date_str.split("-")
            year = datetime.now().year
            return datetime(int(year), int(month), int(day))
        # Formato ISO
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.now()


def parse_number(value: str) -> int:
    """Parse string number (e.g., '113.4K') to int."""
    if not value:
        return 0
    value = value.replace(",", "").replace(".", "")
    if "K" in value.upper():
        return int(float(value.upper().replace("K", "")) * 1000)
    if "M" in value.upper():
        return int(float(value.upper().replace("M", "")) * 1000000)
    try:
        return int(value)
    except:
        return 0


async def import_json_file(file_path: Path):
    """Importa um arquivo JSON para o banco de dados."""
    async with AsyncSessionLocal() as session:
        service = PublicationService(session)
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("Erro: JSON deve ser uma lista de publicações")
            return
        
        print(f"Importando {len(data)} publicações...")
        
        for idx, item in enumerate(data, 1):
            try:
                # Parse comments
                comments = []
                for comment_data in item.get("comments", []):
                    replies = [
                        Reply(
                            username=reply.get("username", ""),
                            text=reply.get("text", ""),
                            likes=parse_number(reply.get("likes", "0")),
                        )
                        for reply in comment_data.get("replies", [])
                    ]
                    
                    comments.append(Comment(
                        username=comment_data.get("username", ""),
                        text=comment_data.get("text", ""),
                        likes=parse_number(comment_data.get("likes", "0")),
                        replies=replies,
                    ))
                
                # Create publication entity
                publication = Publication(
                    publicacao_n=item.get("publicacao_n", idx),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    date=parse_date(item.get("date", "")),
                    views=item.get("views"),
                    likes=item.get("likes"),
                    comments_count=item.get("comments_count", 0),
                    shares=item.get("shares"),
                    bookmarks=item.get("bookmarks"),
                    music_title=item.get("musicTitle"),
                    tags=item.get("tags", []),
                    comments=comments,
                )
                
                await service.create_publication(publication)
                
                if idx % 10 == 0:
                    print(f"Processadas {idx}/{len(data)} publicações...")
                    
            except Exception as e:
                print(f"Erro ao importar publicação {idx}: {e}")
                continue
        
        await session.commit()
        print(f"Importação concluída! {len(data)} publicações processadas.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/import_json.py <caminho_do_json>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Erro: Arquivo {file_path} não encontrado")
        sys.exit(1)
    
    asyncio.run(import_json_file(file_path))

