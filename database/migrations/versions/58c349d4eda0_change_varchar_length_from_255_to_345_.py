"""change varchar length from 255 to 345 for description in arctiles table

Revision ID: 58c349d4eda0
Revises: df147f7d8dc7
Create Date: 2020-07-20 14:22:52.112866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58c349d4eda0'
down_revision = 'df147f7d8dc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'description', new_column_name='description', type_=sa.VARCHAR(length=345))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'description', new_column_name='description', type_=sa.VARCHAR(length=255))
    # ### end Alembic commands ###
