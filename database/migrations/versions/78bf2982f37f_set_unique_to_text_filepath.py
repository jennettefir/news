"""set unique to text_filepath

Revision ID: 78bf2982f37f
Revises: 1dfb169d1178
Create Date: 2020-07-17 13:06:53.026326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78bf2982f37f'
down_revision = '1dfb169d1178'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_articles_text_filepath', table_name='articles')
    op.create_unique_constraint(None, 'articles', ['text_filepath'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'articles', type_='unique')
    op.create_index('ix_articles_text_filepath', 'articles', ['text_filepath'], unique=False)
    # ### end Alembic commands ###