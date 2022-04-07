# Python
from datetime import date
from datetime import datetime

# Sqlalchemy
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String

# Archivos proyecto
from config.db import meta
from config.db import engine


# https://docs.sqlalchemy.org/en/14/core/connections.html


users = Table("users", meta, 
              Column("id", Integer, primary_key=True), 
              Column("name", String(50)), 
              Column("country", String(30)), 
              Column("phone", String(10)), 
              Column("email", String(50)), 
              Column("password", String(50)),
              Column("user_create", String(20)),
              Column("tipo_user", Integer),       
)

meta.create_all(engine)