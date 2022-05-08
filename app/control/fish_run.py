from fastapi import APIRouter
from pydantic import BaseModel

import random
from collections import deque
from datetime import datetime

from models.fish_model import add_oxygen_data_per_minute

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
    oxygen_info['data']=data_temp.date().__str__()
    oxygen_info['time']=data_temp.time().__format__('%H:%M:%S')
    oxygen_info['oxygen']=item.oxygen
    oxygen_info['temperature']=item.temperature
    print("oxygen_info:", oxygen_info)
    add_oxygen_data_per_minute(oxygen_info)
    return {'code':0, 'msg':TEST_DATA}

@router.post('/sendOxygen')
async def add_data(item: OxygenItem):
    data_temp = datetime.now()
    oxygen_info = {}
    oxygen_info['data']=data_temp.date().__str__()
    oxygen_info['time']=data_temp.time().__format__('%H:%M:%S')
    oxygen_info['oxygen']=item.oxygen
    oxygen_info['temperature']=item.temperature
    live_data_deque.append(oxygen_info)
    print("oxygen_info:", oxygen_info)
    # add_oxygen_data_per_minute(oxygen_info)
    return {'code':0, 'msg':TEST_DATA}

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