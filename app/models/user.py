from datetime import datetime, timedelta
from sqlalchemy import Column,Integer,String,Float,Boolean
from sqlalchemy import select
# import sys
# print(sys.path)
from db.database import Base,engine,async_SessionLocal

from loguru import logger
session = async_SessionLocal()

#创建数据模型

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32)) # 用户名
    hashed_password = Column(String(64)) # 哈希密码
    email = Column(String(32)) # 邮箱信息
    disable = Column(Boolean()) # 是否禁用

# def add_login_user(user_info):
#     """ 添加登录用户到数据库 """
#     format_data = User(
#         username=user_info.username,
#         hashed_password=user_info.password,
#         email=user_info.email,
#         disable=user_info.disable
#     )
#     userIndb = session.query(User).filter(User.username==user_info.username).first()
#     if userIndb:
#         return False
#     session.add(format_data)
#     try:
#         session.commit()
#     except Exception as e:
#         logger.warning(str(e))
#         session.rollback()
#     session.refresh(format_data)
#     return True

async def add_login_user(user_info):
    """ 添加登录用户到数据库 """
    format_data = User(
        username=user_info.username,
        hashed_password=user_info.password,
        email=user_info.email,
        disable=user_info.disable
    )
    userIndb = await get_user_info(user_info.username)
    if userIndb:
        return False
    async with async_SessionLocal() as session:
        async with session.begin():
            session.add(format_data)
            # 刷新自带的主键
            await session.flush()
            # 释放该数据
            session.expunge(format_data)
            return True
            

async def get_user_info(username: str) ->User:
    """ 获取用户数据 """
    async with async_SessionLocal() as session:
        sql = select(User).where(User.username==username)
        # logger.debug(f'sql:{sql}')
        result = await session.execute(sql)
        user_info = result.scalars().first()
        # user_info = session.query(User).filter(User.username==username).first()
        return user_info


# Base.metadata.create_all(engine)