"""change description type from varchar to text in articles table

Revision ID: e1e5c916d642
Revises: 58c349d4eda0
Create Date: 2020-07-20 16:13:57.678240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e1e5c916d642'
down_revision = '58c349d4eda0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'description', new_column_name='description', type_=sa.TEXT(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'description', new_column_name='description', type_=sa.VARCHAR(length=345),
                    nullable=False)
    # ### end Alembic commands ###
