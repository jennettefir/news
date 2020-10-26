"""Create table articles

Revision ID: 36784f2d0fda
Revises: 
Create Date: 2020-07-16 15:21:38.090897

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '36784f2d0fda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('link', mysql.VARCHAR(length=768), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('author', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('text_filepath', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('publication_date', mysql.TIMESTAMP(), nullable=False),
    sa.Column('guid', mysql.VARCHAR(length=768), nullable=True),
    sa.Column('atom_link', mysql.VARCHAR(length=768), nullable=True),
    sa.Column('categories', mysql.JSON(), nullable=True),
    sa.Column('image_url', mysql.VARCHAR(length=768), nullable=True),
    sa.Column('credit', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('atom_link'),
    sa.UniqueConstraint('guid'),
    sa.UniqueConstraint('link')
    )
    op.create_index(op.f('ix_articles_text_filepath'), 'articles', ['text_filepath'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_articles_text_filepath'), table_name='articles')
    op.drop_table('articles')
    # ### end Alembic commands ###
