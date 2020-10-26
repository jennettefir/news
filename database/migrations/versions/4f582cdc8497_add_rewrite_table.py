"""add rewrite table

Revision ID: 4f582cdc8497
Revises: 8e8f580dcd24
Create Date: 2020-07-24 10:21:08.540348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4f582cdc8497'
down_revision = '8e8f580dcd24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rewrites',
    sa.Column('id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('article_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('rewrite_type', sa.Enum('translate', 'quillbot', 'gpt2', name='rewritetype'), nullable=False),
    sa.Column('status', mysql.INTEGER(unsigned=True), server_default=sa.text('0'), nullable=False),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('article_id', 'rewrite_type', name='article_id__rewrite_type_UIX')
    )
    op.create_index(op.f('ix_rewrites_article_id'), 'rewrites', ['article_id'], unique=False)
    op.create_index(op.f('ix_rewrites_rewrite_type'), 'rewrites', ['rewrite_type'], unique=False)
    op.create_index(op.f('ix_rewrites_status'), 'rewrites', ['status'], unique=False)
    op.create_index(op.f('ix_rewrites_updated_at'), 'rewrites', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rewrites_updated_at'), table_name='rewrites')
    op.drop_index(op.f('ix_rewrites_status'), table_name='rewrites')
    op.drop_index(op.f('ix_rewrites_rewrite_type'), table_name='rewrites')
    op.drop_index(op.f('ix_rewrites_article_id'), table_name='rewrites')
    op.drop_table('rewrites')
    # ### end Alembic commands ###
