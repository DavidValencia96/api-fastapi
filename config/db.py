from sqlalchemy import create_engine, MetaData


# Conexion de base de datos localx
# engine = create_engine("mysql+pymysql://root:@localhost:3306/api-jd")

# Conexion de base de datos nube
engine = create_engine("mysql+pymysql://bdb0ca6438d403:5d3cde1c@us-cdbr-east-05.cleardb.net/heroku_92dcf5a3cd1744f") 

meta = MetaData()

conn = engine.connect()