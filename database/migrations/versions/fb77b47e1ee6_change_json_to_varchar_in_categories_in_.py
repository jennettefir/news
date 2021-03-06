"""change json to varchar in categories in articles table

Revision ID: fb77b47e1ee6
Revises: 831c95661443
Create Date: 2020-07-20 13:42:40.001017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb77b47e1ee6'
down_revision = '831c95661443'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'categories', new_column_name='categories', type_=sa.VARCHAR(length=255))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'categories', new_column_name='categories', type_=sa.JSON())
    # ### end Alembic commands ###
