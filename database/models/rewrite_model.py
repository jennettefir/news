from articles_scrapers.utils.types import RewriteType
from .base_model import Base
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.types import Enum
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, INTEGER, TEXT
from sqlalchemy.sql import text


class Rewrite(Base):
    __tablename__ = "rewrites"
    id = Column(BIGINT(unsigned=True), primary_key=True, nullable=False)
    article_id = Column(BIGINT(unsigned=True), index=True, nullable=False)
    rewrite_type = Column(Enum(RewriteType), index=True, nullable=False)
    status = Column("status", INTEGER(unsigned=True), unique=False, index=True, nullable=False,
                    server_default=text("0"))
    error = Column("error", TEXT(), index=False, unique=False, nullable=True, default=None)
    created_at = Column("created_at", TIMESTAMP, unique=False, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column("updated_at", TIMESTAMP, unique=False, nullable=False, index=True,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                        server_onupdate=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        UniqueConstraint('article_id', 'rewrite_type', name='article_id__rewrite_type_UIX'),
    )
