from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_URL = "mysql+pymysql://root:@127.0.0.1:3306/fishdata"

engine = create_engine(MYSQL_URL, encoding='utf-8', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()