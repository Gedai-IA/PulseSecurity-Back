"""populate json data

Revision ID: populate_json_data
Revises: create_pub_tables
Create Date: 2025-01-27 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# Importa funções auxiliares
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from helpers import load_all_publications

# revision identifiers, used by Alembic.
revision: str = 'populate_json_data'
down_revision: Union[str, None] = 'create_pub_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Carrega todas as publicações dos arquivos JSON
    publications = load_all_publications()
    
    if not publications:
        print("Nenhuma publicação encontrada nos arquivos JSON.")
        return
    
    print(f"Carregando {len(publications)} publicações...")
    
    # Prepara tabelas para bulk insert
    publications_table = sa.table(
        'publications',
        sa.column('id', sa.Integer),
        sa.column('publicacao_n', sa.Integer),
        sa.column('url', sa.String),
        sa.column('description', sa.Text),
        sa.column('date', sa.DateTime),
        sa.column('views', sa.String),
        sa.column('likes', sa.String),
        sa.column('comments_count', sa.Integer),
        sa.column('shares', sa.String),
        sa.column('bookmarks', sa.String),
        sa.column('music_title', sa.String),
        sa.column('tags', postgresql.JSON),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime)
    )
    
    # Prepara dados das publicações
    publications_data = []
    for pub in publications:
        publications_data.append({
            'publicacao_n': pub['publicacao_n'],
            'url': pub['url'],
            'description': pub['description'],
            'date': pub['date'],
            'views': str(pub.get('views', '')),
            'likes': str(pub.get('likes', '')),
            'comments_count': pub.get('comments_count', 0),
            'shares': str(pub.get('shares', '')),
            'bookmarks': str(pub.get('bookmarks', '')),
            'music_title': pub.get('music_title', ''),
            'tags': pub.get('tags', []),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })
    
    # Insere publicações
    op.bulk_insert(publications_table, publications_data)
    print(f"Inseridas {len(publications_data)} publicações.")
    
    # Obtém os IDs das publicações inseridas
    # Como usamos bulk_insert, precisamos fazer uma query para obter os IDs
    connection = op.get_bind()
    
    # Insere comentários e respostas por publicação para manter a ordem correta
    comments_table = sa.table(
        'comments',
        sa.column('id', sa.Integer),
        sa.column('publication_id', sa.Integer),
        sa.column('username', sa.String),
        sa.column('text', sa.Text),
        sa.column('likes', sa.Integer),
        sa.column('created_at', sa.DateTime)
    )
    
    replies_table = sa.table(
        'replies',
        sa.column('id', sa.Integer),
        sa.column('comment_id', sa.Integer),
        sa.column('username', sa.String),
        sa.column('text', sa.Text),
        sa.column('likes', sa.Integer),
        sa.column('created_at', sa.DateTime)
    )
    
    total_comments = 0
    total_replies = 0
    
    # Processa cada publicação individualmente para manter a ordem dos comentários
    for pub in publications:
        # Obtém o ID real da publicação usando publicacao_n
        result = connection.execute(
            sa.text("SELECT id FROM publications WHERE publicacao_n = :pub_n"),
            {"pub_n": pub['publicacao_n']}
        )
        pub_row = result.fetchone()
        if not pub_row:
            continue
        
        publication_id = pub_row[0]
        
        # Insere comentários desta publicação
        comments_data = []
        for comment in pub['comments']:
            comments_data.append({
                'publication_id': publication_id,
                'username': comment['username'],
                'text': comment['text'],
                'likes': comment['likes'],
                'created_at': datetime.now()
            })
        
        if comments_data:
            op.bulk_insert(comments_table, comments_data)
            total_comments += len(comments_data)
            
            # Obtém os IDs dos comentários recém-inseridos (na ordem de inserção)
            comment_ids_result = connection.execute(
                sa.text("""
                    SELECT id FROM comments 
                    WHERE publication_id = :pub_id 
                    ORDER BY id DESC 
                    LIMIT :limit
                """),
                {"pub_id": publication_id, "limit": len(comments_data)}
            )
            comment_ids = [row[0] for row in comment_ids_result.fetchall()]
            comment_ids.reverse()  # Reverte para ter a ordem correta
            
            # Insere respostas para cada comentário
            replies_data = []
            for comment_idx, comment in enumerate(pub['comments']):
                if comment_idx < len(comment_ids):
                    comment_id = comment_ids[comment_idx]
                    for reply in comment['replies']:
                        replies_data.append({
                            'comment_id': comment_id,
                            'username': reply['username'],
                            'text': reply['text'],
                            'likes': reply['likes'],
                            'created_at': datetime.now()
                        })
            
            if replies_data:
                op.bulk_insert(replies_table, replies_data)
                total_replies += len(replies_data)
    
    print(f"Inseridos {total_comments} comentários e {total_replies} respostas.")


def downgrade() -> None:
    # Remove todos os dados inseridos
    op.execute("DELETE FROM replies")
    op.execute("DELETE FROM comments")
    op.execute("DELETE FROM publications")

