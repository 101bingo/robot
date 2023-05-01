from collections import deque
from datetime import datetime, timedelta
from loguru import logger

# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from models.fish_model import add_oxygen_data_per_minute,add_oxygen_warning_data
from control.weixin import oxygen_threading, init_warning_flag, get_global_access_token, is_stop_warning, LIMIT_OXYGEN

# LIMIT_OXYGEN = 5
LOW_COUNT = 0
THRESHOLD_VALUE = 5 #低于阈值时间（单位分钟）

async def write_mysql_data(msg: deque, start_time: datetime):
    global LOW_COUNT
    data_to_mysql = dict()
    while msg:
        data = msg.popleft()
        # timeNow, temper, oxygen_perc, oxygen, count_time, is_ready_flag
        date_time = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')
        data_to_mysql['date_time'] = date_time
        data_to_mysql['temperature'] = data[1]
        data_to_mysql['oxygen_perc'] = data[2]
        data_to_mysql['oxygen'] = data[3]
        data_to_mysql['oxygen_limit'] = LIMIT_OXYGEN
        logger.warning(f'LIMIT_OXYGEN1:{LIMIT_OXYGEN}')
        if date_time>(start_time+timedelta(minutes=1)):
            start_time = date_time
            # logger.warning(f'LOW_COUNT:{LOW_COUNT}')
            logger.warning(f'LIMIT_OXYGEN2:{LIMIT_OXYGEN}')
            if data_to_mysql['oxygen']<LIMIT_OXYGEN:
                LOW_COUNT += 1
            else:
                LOW_COUNT = 0
            logger.warning(f'LIMIT_OXYGEN:{LIMIT_OXYGEN}')
            logger.warning(f'LOW_COUNT:{LOW_COUNT}')
            if LOW_COUNT==THRESHOLD_VALUE and not is_stop_warning:
                oxygen_threading(date_time, data[3], data[1])
                await add_oxygen_warning_data(data_to_mysql)
                LOW_COUNT = 0
            logger.debug('start add data to mysql')
            await add_oxygen_data_per_minute(data_to_mysql) #添加到数据库
            logger.debug('end add data to mysql')

""" 每6小时初始化停止报警的标识 """
async def init_stopflag_per_six_hours():
    logger.debug('start init_stopflag_per_six_hours')
    init_warning_flag()
    logger.debug(f'is_stop_warning:{is_stop_warning}')

""" 每2小时获取一次access token """
async def init_access_token():
    logger.debug('get new access token')
    get_global_access_token()

scheduler = None
def init_scheduler(msg_que: deque):
    start_time = datetime.now()
            
    """ 初始化 """
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor()
    }
    job_defaults = {
        'coalesce': True,
        'max_instance': 1
    }
    global scheduler
    scheduler = AsyncIOScheduler()
    # scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    # 写数据库任务，每1分钟存储一次数据
    scheduler.add_job(func=write_mysql_data, args=(msg_que, start_time), trigger='interval', minutes=1)
    # 初始化任务，每6小时初始化停止报警的标识
    scheduler.add_job(func=init_stopflag_per_six_hours, trigger='interval', hours=6)
    # 初始化任务，每2小时获取一次access token
    scheduler.add_job(func=init_access_token, trigger='interval', hours=2)
    # 启动调度器
    scheduler.start()
    logger.debug('end init scheduler')