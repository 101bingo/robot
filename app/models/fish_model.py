from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.sql.expression import column, true

from db.database import Base

#创建数据模型

class FishData(Base):
    __tablename__ = "fish"
    id = Column(Integer, primary_key=True, index=True)
    date_info = Column(String(32)) # 日期信息，年月日
    time_info = Column(String(32)) # 时间信息，时分秒
    oxygen_data = Column(Float(4)) # 氧气数据
    temperature_data = Column(Float(4)) # 温度数据