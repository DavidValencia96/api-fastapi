from sqlalchemy import create_engine, MetaData

# engine = create_engine("mysql+pymysql://root:@localhost:3306/api-jd")
engine = create_engine("mysql+pymysql://b5a3c397ee901e:605edb7e@us-cdbr-east-05.cleardb.net/heroku_705c666e6924547")

meta = MetaData()

conn = engine.connect()