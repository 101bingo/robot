from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

MYSQL_URL = "mysql+aiomysql://root:Xu123456@127.0.0.1:3306/fishdata"
# MYSQL_URL = "mysql+aiomysql://root@127.0.0.1:3306/fishdata"

# engine = create_engine(MYSQL_URL, encoding='utf-8', echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
""" 数据库异步操作 """
engine = create_async_engine(MYSQL_URL, encoding='utf-8', echo=True, poolclass=NullPool)

async_SessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

Base = declarative_base()