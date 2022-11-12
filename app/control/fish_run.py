from fastapi import APIRouter
from pydantic import BaseModel

import random
from collections import deque
from datetime import datetime, timedelta
from loguru import logger

from models.fish_model import add_oxygen_data_per_minute,get_oxygen_data_onehour,get_oxygen_data_days

# 实际的子路由
router = APIRouter()

TEST_DATA = []
DATA_INDEX = 0

cmd_deque = deque()       # 指令队列
live_data_deque = deque() # 实时数据队列

class OxygenItem(BaseModel):
    oxygen: float
    temperature: float

class LiveOxygenItem(BaseModel):
    oxygen: float


@router.get('/test')
async def test_fun():
    return {'msg':'靓仔，雷猴','code':'success'}

@router.post('/addData')
async def add_data(item: OxygenItem):
    global DATA_INDEX,TEST_DATA
    data_temp = datetime.now()
    oxygen_info = {}
    oxygen_info['date_time']=data_temp
    # oxygen_info['data']=data_temp.date().__str__()
    # oxygen_info['time']=data_temp.time().__format__('%H:%M:%S')
    oxygen_info['oxygen']=item.oxygen
    oxygen_info['temperature']=item.temperature
    print("oxygen_info:", oxygen_info)
    await add_oxygen_data_per_minute(oxygen_info)
    return {'code':0, 'msg':TEST_DATA}

@router.post('/sendOxygen')
async def add_data(item: OxygenItem):
    data_temp = datetime.now() - timedelta(days=15)
    oxygen_info = {}

    # live_data_deque.append(oxygen_info)
    # print("oxygen_info:", oxygen_info)
    for n in range(1,1001):
        nowdate = data_temp - timedelta(minutes=5*n)
        oxygen_info['date_time']=nowdate
        oxygen_info['oxygen']=round(random.uniform(5,30), 1)
        oxygen_info['temperature']=round(random.uniform(5,40), 1)
        await add_oxygen_data_per_minute(oxygen_info)
    return {'code':0, 'msg':TEST_DATA}

@router.get('/getOxygenOneHour')
async def getOxygenOneHour(hours: int):
    data_temp = await get_oxygen_data_onehour(hours)
    logger.debug(str(data_temp))
    logger.debug(len(data_temp))
    logger.debug([res.oxygen_data for res in data_temp])
    res = [[res.date_time.__str__(), res.oxygen_data] for res in data_temp]
    logger.debug([[res.date_time.__str__(), res.oxygen_data] for res in data_temp])
    return {'code':0, 'msg':'success', 'data':res}

@router.get('/getOxygendays/')
async def getOxygendays(startDay: int, endDay: int):
    start = datetime.fromtimestamp(startDay)
    end = datetime.fromtimestamp(endDay)
    logger.debug(f'start:{start}')
    logger.debug(f'end:{end}')
    data_temp = await get_oxygen_data_days(start, end)
    logger.debug(str(data_temp))
    logger.debug(len(data_temp))
    logger.debug([res.oxygen_data for res in data_temp])
    res = [[res.date_time.__str__(), res.oxygen_data] for res in data_temp]
    logger.debug([[res.date_time.__str__(), res.oxygen_data] for res in data_temp])
    return {'code':0, 'msg':'success', 'data':res}

@router.get('/addData2')
async def add_data2():
    global DATA_INDEX,TEST_DATA
    n = random.randint(1,10)
    DATA_INDEX += 1
    TEST_DATA.append({'index':DATA_INDEX, 'value':n})
    return {'code':0, 'msg':TEST_DATA}

@router.get('/startEngine1')
async def start_engine_bone1():
    cmd_deque.append('0x600x600x01')

@router.get('/stopEngine1')
async def stop_engine_bone1():
    cmd_deque.append('0x600x600x02')