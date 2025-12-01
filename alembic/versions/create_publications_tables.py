"""create publications tables

Revision ID: create_pub_tables
Revises: 9eaec19212fd
Create Date: 2025-01-27 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'create_pub_tables'
down_revision: Union[str, None] = '9eaec19212fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    """Verifica se uma tabela já existe no banco de dados."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()


def upgrade() -> None:
    # Create publications table
    if not table_exists('publications'):
        op.create_table(
            'publications',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('publicacao_n', sa.Integer(), nullable=False),
            sa.Column('url', sa.String(), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('date', sa.DateTime(), nullable=False),
            sa.Column('views', sa.String(), nullable=True),
            sa.Column('likes', sa.String(), nullable=True),
            sa.Column('comments_count', sa.Integer(), server_default='0'),
            sa.Column('shares', sa.String(), nullable=True),
            sa.Column('bookmarks', sa.String(), nullable=True),
            sa.Column('music_title', sa.String(), nullable=True),
            sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_publications_id'), 'publications', ['id'], unique=False)
        op.create_index(op.f('ix_publications_publicacao_n'), 'publications', ['publicacao_n'], unique=True)
        op.create_index(op.f('ix_publications_date'), 'publications', ['date'], unique=False)

    # Create comments table
    if not table_exists('comments'):
        op.create_table(
            'comments',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('publication_id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(), nullable=False),
            sa.Column('text', sa.Text(), nullable=False),
            sa.Column('likes', sa.Integer(), server_default='0'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['publication_id'], ['publications.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)

    # Create replies table
    if not table_exists('replies'):
        op.create_table(
            'replies',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('comment_id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(), nullable=False),
            sa.Column('text', sa.Text(), nullable=False),
            sa.Column('likes', sa.Integer(), server_default='0'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_replies_id'), 'replies', ['id'], unique=False)

    # Create publication_analyses table
    if not table_exists('publication_analyses'):
        op.create_table(
            'publication_analyses',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('publication_id', sa.Integer(), nullable=False),
            sa.Column('main_sentiment', sa.String(), nullable=False),
            sa.Column('main_emotion', sa.String(), nullable=False),
            sa.Column('main_topic', sa.String(), nullable=False),
            sa.Column('analyzed_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['publication_id'], ['publications.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('publication_id')
        )
        op.create_index(op.f('ix_publication_analyses_id'), 'publication_analyses', ['id'], unique=False)

    # Create comment_analyses table
    if not table_exists('comment_analyses'):
        op.create_table(
            'comment_analyses',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('comment_id', sa.Integer(), nullable=False),
            sa.Column('sentiment', sa.String(), nullable=False),
            sa.Column('emotion', sa.String(), nullable=False),
            sa.Column('topic', sa.String(), nullable=False),
            sa.Column('analyzed_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('comment_id')
        )
        op.create_index(op.f('ix_comment_analyses_id'), 'comment_analyses', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_comment_analyses_id'), table_name='comment_analyses')
    op.drop_table('comment_analyses')
    op.drop_index(op.f('ix_publication_analyses_id'), table_name='publication_analyses')
    op.drop_table('publication_analyses')
    op.drop_index(op.f('ix_replies_id'), table_name='replies')
    op.drop_table('replies')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_publications_date'), table_name='publications')
    op.drop_index(op.f('ix_publications_publicacao_n'), table_name='publications')
    op.drop_index(op.f('ix_publications_id'), table_name='publications')
    op.drop_table('publications')

