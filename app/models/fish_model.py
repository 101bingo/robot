from logging import exception
from sqlalchemy import Column,Integer,String,Float
# import sys
# print(sys.path)
from db.database import Base,engine,SessionLocal

import logging
session = SessionLocal()

#创建数据模型

class FishData(Base):
    __tablename__ = "fish"
    id = Column(Integer, primary_key=True, index=True)
    oxygen_data = Column(Float(4)) # 氧气数据
    temperature_data = Column(Float(4)) # 温度数据
    date_info = Column(String(32)) # 日期信息，年月日
    time_info = Column(String(32)) # 时间信息，时分秒

def add_oxygen_data_per_minute(oxygen_info):
    """ 每分钟添加溶氧数据到数据库 """
    format_data = FishData(
        oxygen_data=oxygen_info['oxygen'],
        temperature_data=oxygen_info['temperature'],
        date_info=oxygen_info['data'],
        time_info=oxygen_info['time']
    )
    session.add(format_data)
    try:
        session.commit()
    except Exception as e:
        logging.warning(str(e))
        session.rollback()
    session.refresh(format_data)
    return True

# Base.metadata.create_all(engine)