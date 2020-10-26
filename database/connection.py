import sqlalchemy as db
from articles_scrapers.utils import create_mysql_conn_string


engine = db.create_engine(create_mysql_conn_string())
