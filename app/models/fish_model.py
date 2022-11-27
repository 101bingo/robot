from datetime import datetime, timedelta
from logging import exception
from sqlalchemy import Column,Integer,String,Float,DateTime
from sqlalchemy import select
# import sys
# print(sys.path)
from db.database import Base,engine,async_SessionLocal

from loguru import logger
session = async_SessionLocal()
# session = SessionLocal()

#创建数据模型

class FishData(Base):
    """ 记录溶氧数据 """
    __tablename__ = "fish"
    id = Column(Integer, primary_key=True, index=True)
    oxygen_data = Column(Float(4)) # 溶氧值数据
    oxygen_perc = Column(Float(4)) # 溶氧比数据
    temperature = Column(Float(4)) # 温度数据
    # date_info = Column(String(32)) # 日期信息，年月日
    # time_info = Column(String(32)) # 时间信息，时分秒
    date_time = Column(DateTime())

class OxygenLimitRecord(Base):
    """ 记录氧限设置记录 """
    __tablename__ = "oxygenlimitrecord"
    id = Column(Integer, primary_key=True, index=True)
    device_info = Column(String(32)) # 设备信息
    oxygen_limit = Column(Float(4)) # 氧限数据
    date_time = Column(DateTime())  # 设置时间

class OxygenWarningRecord(Base):
    """ 记录氧限报警记录 """
    __tablename__ = "oxygenwarningrecord"
    id = Column(Integer, primary_key=True, index=True)
    oxygen_data = Column(Float(4)) # 溶氧值数据
    oxygen_perc = Column(Float(4)) # 溶氧比数据
    temperature = Column(Float(4)) # 温度数据
    oxygen_limit = Column(Float(4)) # 氧限数据
    date_time = Column(DateTime())  # 设置时间

async def add_oxygen_data_per_minute(oxygen_info):
    """ 每分钟添加溶氧数据到数据库 """
    format_data = FishData(
        oxygen_data=oxygen_info['oxygen'],
        temperature=oxygen_info['temperature'],
        # date_info=oxygen_info['data'],
        oxygen_perc=oxygen_info['oxygen_perc'],
        date_time=oxygen_info['date_time']
    )

    async with async_SessionLocal() as session:
        async with session.begin():
            session.add(format_data)
            # 刷新自带的主键
            await session.flush()
            # 释放该数据
            session.expunge(format_data)
            return True


# def add_oxygen_data_per_minute(oxygen_info):
#     """ 每分钟添加溶氧数据到数据库 """
#     format_data = FishData(
#         oxygen_data=oxygen_info['oxygen'],
#         temperature_data=oxygen_info['temperature'],
#         date_info=oxygen_info['data'],
#         time_info=oxygen_info['time']
#     )
#     session.add(format_data)
#     try:
#         session.commit()
#     except Exception as e:
#         logging.warning(str(e))
#         session.rollback()
#     session.refresh(format_data)
#     return True

async def get_oxygen_data_onehour(hours: int):
    """ 获取一小时内数据 """
    time_now = datetime.now()
    # onehourData = session.query(FishData).filter(FishData.date_info <=time_now-timedelta(hours=1)).all()
    args = {'hours': hours}

    async with async_SessionLocal() as session:
        sql = select(FishData).where(FishData.date_time>=time_now-timedelta(**args))
        # logger.debug(f'sql:{sql}')
        result = await session.execute(sql)
        data_info = result.scalars().all()
        return data_info

async def get_oxygen_data_days(startday: datetime, endday: datetime):
    """ 获取日期内数据 """
    # time_now = datetime.now()
    # args = {'days': startday}

    async with async_SessionLocal() as session:
        sql = select(FishData).where(FishData.date_time>=startday).where(FishData.date_time<endday)
        # logger.debug(f'sql:{sql}')
        result = await session.execute(sql)
        data_info = result.scalars().all()
        return data_info

async def add_setting_oxygen_limit_data(oxygen_info):
    """ 设置氧限的操作写数据库 """
    format_data = OxygenLimitRecord(
        oxygen_limit=oxygen_info['oxygen_limit'],
        device_info=oxygen_info['device_info'],
        date_time=oxygen_info['date_time']
    )

    async with async_SessionLocal() as session:
        async with session.begin():
            session.add(format_data)
            # 刷新自带的主键
            await session.flush()
            # 释放该数据
            session.expunge(format_data)
            return True

async def get_setting_oxygen_limit_data():
    """ 读取氧限的操作记录 """
    async with async_SessionLocal() as session:
        sql = select(OxygenLimitRecord).order_by(OxygenLimitRecord.id.desc())
        result = await session.execute(sql)
        data_info = result.scalars().all()
        return data_info

async def add_oxygen_warning_data(oxygen_info):
    """ 溶氧报警 写数据库 """
    format_data = OxygenWarningRecord(
        oxygen_data=oxygen_info['oxygen'],
        oxygen_perc=oxygen_info['oxygen_perc'],
        temperature=oxygen_info['temperature'],
        oxygen_limit=oxygen_info['oxygen_limit'],
        date_time=oxygen_info['date_time']
    )

    async with async_SessionLocal() as session:
        async with session.begin():
            session.add(format_data)
            # 刷新自带的主键
            await session.flush()
            # 释放该数据
            session.expunge(format_data)
            return True

async def get_oxygen_warning_data():
    """ 读取溶氧报警的记录 """
    async with async_SessionLocal() as session:
        sql = select(OxygenWarningRecord).order_by(OxygenWarningRecord.id.desc()) #.limit(10)
        result = await session.execute(sql)
        data_info = result.scalars().all()
        return data_info
# Base.metadata.create_all(engine)