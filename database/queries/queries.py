from typing import List, Tuple, Dict

from sqlalchemy.dialects.mysql import insert
from sqlalchemy import update, and_
from sqlalchemy.sql import select

from articles_scrapers.utils.types import RewriteType
from articles_scrapers.utils.constants import STATUS_IN_PROGRESS
from database.connection import engine
from database.models import Article, Rewrite
from datetime import datetime


def add_article(item):
    insert_sql = insert(Article).values(
        title=item['title'],
        link=item['link'],
        description=item['description'],
        author=item.get('author', None),
        text_filepath=item['text_filepath'],
        publication_date=datetime.strptime(item['publication_date'], "%a, %d %b %Y %H:%M:%S %z"),
        guid=item.get('guid', None),
        categories=item.get('categories', None),
        image_url=item.get('image_url'),
        credit=item.get('credit'),
    )

    insert_sql_on_update = insert_sql.on_duplicate_key_update(
        title=insert_sql.inserted.title,
        description=insert_sql.inserted.description,
        author=insert_sql.inserted.author,
        text_filepath=insert_sql.inserted.text_filepath,
        publication_date=insert_sql.inserted.publication_date,
        guid=insert_sql.inserted.guid,
        categories=insert_sql.inserted.categories,
        image_url=insert_sql.inserted.image_url,
        credit=insert_sql.inserted.credit
    )

    engine.connect().execute(insert_sql_on_update)


def select_unprocessed_rewrites(rewrite_type: RewriteType):
    select_sql = select([Article.id, Article.text_filepath, Article.title, Article.publication_date]) \
        .where(Article.id.notin_(
        select([Rewrite.article_id])
            .where(Rewrite.rewrite_type == rewrite_type.name)
    ))

    result_proxy = engine.connect().execute(select_sql)
    return tuple(dict(record) for record in result_proxy)


def insert_in_progress_rewrite(rewrite_type: RewriteType, article_ids: Tuple[int], status: int = STATUS_IN_PROGRESS):
    for article_id in article_ids:
        insert_sql = insert(Rewrite).values(
            article_id=article_id,
            rewrite_type=rewrite_type.name,
            status=status,
        )

        insert_sql_on_update = insert_sql.on_duplicate_key_update(
            status=status
        )

        engine.connect().execute(insert_sql_on_update)


def update_in_progress_rewrite(row: Dict):
    update_sql = update(Rewrite) \
        .where(and_(Rewrite.article_id == row['article_id'], Rewrite.rewrite_type == row['rewrite_type'])) \
        .values(
        error=row['error'],
        status=row['status'],
    )
    engine.connect().execute(update_sql)
