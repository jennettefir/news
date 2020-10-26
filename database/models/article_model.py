from .base_model import Base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, TIMESTAMP, DATETIME, TEXT
from sqlalchemy.sql import text


class Article(Base):
    __tablename__ = "articles"
    id = Column(BIGINT(unsigned=True), primary_key=True, nullable=False)
    title = Column(VARCHAR(length=255), nullable=False)
    link = Column(VARCHAR(length=768), nullable=False, unique=True)
    description = Column(TEXT, nullable=False)
    author = Column(VARCHAR(length=255))
    text_filepath = Column(VARCHAR(length=255), nullable=False)
    publication_date = Column(DATETIME, nullable=False)
    guid = Column(VARCHAR(length=768))
    categories = Column(TEXT)
    image_url = Column(VARCHAR(length=768))
    credit = Column(VARCHAR(length=255))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

