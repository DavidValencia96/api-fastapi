# Python
from datetime import date
from datetime import datetime

# Sqlalchemy
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String

# Archivos proyecto
from config.db import meta
from config.db import engine

tweetsModel = Table("tweet", meta, 
              Column("tweet_id", Integer, primary_key=True), 
              Column("content", String(255)), 
              Column("create_tw_date", String(30)), 
              Column("update_tw_date", String(30)), 
              Column("user_id_create", Integer)
)

meta.create_all(engine)