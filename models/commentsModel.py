# Python
from datetime import date
from datetime import datetime

# Sqlalchemy
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String

# Archivos proyecto
from config.db import meta
from config.db import engine

commentsModel = Table("comments",meta,
                      Column("comment_id", Integer, primary_key=True),
                      Column("tweet_id", Integer),
                      Column("comment_content", String(255)),
                      Column("cm_create_date", String(30)),
                      Column("cm_update_date", String(30)),
                      Column("user_id_comment", Integer)
)

meta.create_all(engine)