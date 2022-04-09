from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://id18513416_juandavidfastapi:m\2+)nCMrgH6xeRd@https://databases-auth.000webhost.com/index.php/id18513416_fastapi")

meta = MetaData()

conn = engine.connect()
