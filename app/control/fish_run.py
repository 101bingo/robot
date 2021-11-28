from fastapi import APIRouter

import random

# 实际的子路由
router = APIRouter()

TEST_DATA = []
DATA_INDEX = 0

@router.get('/test')
async def test_fun():
    return {'msg':'靓仔，雷猴','code':'success'}

@router.get('/addData')
async def add_data():
    global DATA_INDEX,TEST_DATA
    return {'code':0, 'msg':TEST_DATA}

@router.get('/addData2')
async def add_data2():
    global DATA_INDEX,TEST_DATA
    n = random.randint(1,10)
    DATA_INDEX += 1
    TEST_DATA.append({'index':DATA_INDEX, 'value':n})
    return {'code':0, 'msg':TEST_DATA}