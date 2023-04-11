from datetime import datetime,time
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET,socket
from fastapi import FastAPI,WebSocket, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from fastapi_mqtt import FastMQTT,MQTTConfig

import random
from loguru import logger
import uvicorn
import asyncio
import time
import threading
import multiprocessing
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from router.api import api_router
from control.fish_run import cmd_deque,live_data_deque

from control.login import *
from control.ws import manager
from scheduler.write_mysql_job import init_scheduler

logger.add('/var/log/robot/service.log', rotation='50 MB')
# logger.add(r'F:\WORK\code\debug\service.log', rotation='50 MB')
tcp_deque = deque()       # tcp消息队列
tcp_deque_backup = deque()       # tcp消息队列备份
ota_pkg_queue = deque()       # ota分包队列
# pressure_deque = deque() #室温，大气压值
# tcp_deque = multiprocessing.Queue()       # tcp消息队列
IS_TCP_START = 0
RESTART_FLAG = 0

app = FastAPI()
# 入口添加api_router
app.include_router(api_router, prefix="/api")


origins = [
    'http://localhost:9528',
    'http://localhost',
    'http://localhost:8080',
    'http://42.193.138.254'
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

mqtt_config = MQTTConfig(
    host='42.193.138.254',
    port='1883',
    keepalive=60,
    username='abc',
    password='a123'
)

mqtt = FastMQTT(
    config=mqtt_config
)
mqtt.init_app(app)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    # mqtt.client.subscribe('LG8VRHZ5VR9LXK7C111A')
    mqtt.client.subscribe('/fishmonitor/otaupgrade')
    mqtt.client.subscribe('/fishmonitor/msg')
    mqtt.client.subscribe('/fishmonitor/wethers')
    mqtt.client.subscribe('/fishmonitor/oxygen')
    logger.warning(f'Connected:{client} {flags} {rc} {properties}')

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    # print("Received message: ", datetime.now(),topic, payload, qos, properties)
    if topic=='/fishmonitor/msg':
        if payload.decode()=='PKGACK':
            if ota_pkg_queue:
                pkg = ota_pkg_queue.popleft()
                mqtt.publish("/fishmonitor/otaupgrade", pkg)
            else:
                mqtt.publish("/fishmonitor/otaupgrade", bytes.fromhex("aa01aa01"))
        else:
            logger.warning(payload.decode())
    # 处理气压信息，备份
    # if topic=='/fishmonitor/wethers': #get wether info
    #     wether_info = str(payload, encoding='utf8')
    #     # print('wether info:', wether_info)
    #     temperature_air, pressure = wether_info.split(',')
    #     temperature_air = float(temperature_air)
    #     pressure = float(pressure)
    #     pressure_deque.append([temperature_air, pressure])
    if topic=='/fishmonitor/oxygen':
        payload = payload.decode()
        *newload,tpAir,press = payload.split(',')
        hex_data = [f'{hex(int(i,10))[2:]:0>2}' for i in newload]

        func_key = hex_data[1]
        if func_key in ['03']:
            timeNow = datetime.now()
            timeNow = datetime.strftime(timeNow, '%Y-%m-%d %H:%M:%S')
            # temper = round(int(hex_data[6:10], 16)/100.0 - 50, 2)          #温度值
            # oxygen_perc = int(hex_data[14:18], 16)/100.0    #溶氧比
            # oxygen = int(hex_data[22:26], 16)/100.0         #溶氧值
            # count_time = int(hex_data[30:34],16)                   #倒计时
            # is_ready_flag = int(hex_data[34:38],16)                #标识位
            temper = round(int(''.join(hex_data[3:5]), 16)/100.0 - 50, 2)          #温度值
            oxygen_perc = int(''.join(hex_data[7:9]), 16)/100.0    #溶氧比
            oxygen = int(''.join(hex_data[11:13]), 16)/100.0         #溶氧值
            count_time = int(''.join(hex_data[15:17]),16)                   #倒计时
            is_ready_flag = int(''.join(hex_data[17:19]),16)                #标识位
            tpAir = round(float(tpAir), 2)          #温度值
            press = round(float(press)/100, 2)          #大气压hPa
            total_data = [timeNow, temper, oxygen_perc, oxygen, count_time, is_ready_flag, tpAir, press]
            tcp_deque.append(total_data)
            tcp_deque_backup.append(total_data)
            # logger.debug(tcp_deque)
        else:
            logger.warning(f'响应数据异常：{payload}')

@app.get("/publishmsg")
async def publish_message():
    # mqtt.publish("LG8VRHZ5VR9LXK7C111A", "Hello from Fastapi") #publishing mqtt topic
    mqtt.publish("/fishmonitor/otaupgrade", "restartboot") #publishing mqtt topic

    return {"result": True,"message":"Published" }

@app.post("/otaupdate")
async def ota_update(file: UploadFile):
    from zlib import crc32
    RECORD_SIZE = 100
    ota_pkg_queue.clear()
    filecontent = file.file.read()
    file_len = len(filecontent)
    filename = file.filename
    save_path = f'F:\ota_test\{filename}'
    CRC_VAVLUE = crc32(filecontent, 0) #CRC32校验值
    OTA_START = 'ff55ff55'
    OTA_HEAD = f'{OTA_START}{CRC_VAVLUE:08x}{file_len:04x}'

    with open(save_path, 'wb') as f:
        f.write(filecontent)
    with open(save_path, 'r', encoding='utf8') as f:
        records = iter(partial(f.read, RECORD_SIZE), '')
        for r in records:
            ota_pkg_queue.append(r)
    
    # msg = bytes.fromhex('ff55ff55d250d0ab19bd')
    msg = bytes.fromhex(OTA_HEAD)
    mqtt.publish("/fishmonitor/otaupgrade", msg)

    return {"result": True,"message":"Published" }

@app.post("/uploadfile/")
async def create_uploadfile(file: UploadFile):
    filecontent = file.file.read()
    filename = file.filename
    save_path = f'F:\ota_test\{filename}'
    with open(save_path, 'wb') as f:
        f.write(filecontent)
    return {'filename': file.filename}

@app.on_event('startup')
def init_scheduler_before():
    """ 初始化定时任务 """
    logger.debug('start init scheduler')
    init_scheduler(tcp_deque_backup)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    msg_key = ['date_time', 'temper', 'oxygen_perc', 'oxygen', 'count_time','is_ready_flag', 'temp_air', 'pressure']
    while True:
        if tcp_deque:
            msg = tcp_deque.popleft()
            data_dict = dict(zip(msg_key, msg))
            await manager.broadcast(data_dict)
        else:
            await asyncio.sleep(0.01)

@app.websocket("/livedata")
async def websocket_send(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            if data:
                final_data = data.split(',')
                final_data = [int(dn) for dn in final_data]
                logger.info(f'data:{final_data}\n{type(final_data)}')
                if len(final_data) ==2:
                    live_data_deque.append(final_data)
                    if len(live_data_deque)>10:
                        live_data_deque.popleft()
    except Exception as e:
        await websocket.close()

@app.get('/testtcp')
def testtcprecv():
    if tcp_deque:
        logger.debug(f'tcp_deque:{tcp_deque}')
    else:
        logger.debug('tcp deque is empty')

@app.get('/testrestart')
def test_restart():
    global RESTART_FLAG
    RESTART_FLAG = 1

@app.get('/addtcpdata')
async def add_tcp_data():
    import random
    timeNow = datetime.now()
    timeNow = datetime.strftime(timeNow, '%Y-%m-%d %H:%M:%S')
    temper = round(random.uniform(20, 30), 2)
    oxygen_perc = round(random.uniform(98, 120), 2)
    oxygen = round(random.uniform(1, 5), 2)
    count_time = random.randint(0,5)
    is_ready_flag = random.choice([0,1])
    tcp_deque.append([timeNow, temper, oxygen_perc, oxygen, count_time, is_ready_flag])
    tcp_deque_backup.append([timeNow, temper, oxygen_perc, oxygen, count_time, is_ready_flag])

@app.get('/startTcp')
def start_tcp_server():
    global IS_TCP_START,tcp_deque
    if IS_TCP_START:
        return {'res':0, 'msg':'tcp server is already started'}
    else:
        IS_TCP_START = 1
        thd_tcp = threading.Thread(target=tcpworker)
        thd_tcp.setDaemon(True) #设置守护线程(主线程关闭后，子线程自动销毁)
        thd_tcp.start()

@app.get('/stopTcp')
def stop_tcp_server():
    global IS_TCP_START,thd_tcp
    if IS_TCP_START:
        return {'res':0, 'msg':'tcp server is already closed'}

def server():
    HOST = '0.0.0.0'
    PORT = 8002
    uvicorn.run(app='main:app', host=HOST, port=PORT, reload=True, debug=True, workers=1)

def recv_msg(tcp_client, client_address):
    while True:
        try:
            client_text = tcp_client.recv(64)
            if client_text:
                logger.debug(f'client_text_length:{len(client_text)}')
                logger.debug(f'[{client_address}]->recv:{client_text}')
                # continue
                hex_data = client_text.hex()
                func_key = hex_data[2:4]
                if func_key in ['03']:
                    timeNow = datetime.now()
                    timeNow = datetime.strftime(timeNow, '%Y-%m-%d %H:%M:%S')
                    temper = round(int(hex_data[6:10], 16)/100.0 - 50, 2)          #温度值
                    oxygen_perc = int(hex_data[14:18], 16)/100.0    #溶氧比
                    oxygen = int(hex_data[22:26], 16)/100.0         #溶氧值
                    count_time = int(hex_data[30:34],16)                   #倒计时
                    is_ready_flag = int(hex_data[34:38],16)                #标识位
                    total_data = [timeNow, temper, oxygen_perc, oxygen, count_time, is_ready_flag]
                    tcp_deque.append(total_data)
                    tcp_deque_backup.append(total_data)
                else:
                    logger.warning(f'响应数据异常：{client_text}')
            else:
                logger.debug(f'[{client_address}]->status:已下线')
                logger.debug(f"client_text:{client_text}")
                tcp_client.close()
                break
        except ConnectionResetError: # 捕捉客户端异常断开
            logger.debug(f'[{client_address}]->status:已断开连接')
            tcp_client.close()
            break

def tcpworker():
    pool = ThreadPoolExecutor(10) # 最大客户端连接个数10
    SERVER_PORT = 6111
    tcp_server = socket(AF_INET, SOCK_STREAM)
    #设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    # tcp_server.setsockopt(SOL_SOCKET, SO_KEEPALIVE, True)
    # tcp_server.ioctl(
    #     SIO_KEEPALIVE_VALS,(1,60*1000,30*1000)
    # )

    #绑定端口
    tcp_server.bind(('', SERVER_PORT))
    tcp_server.listen(4)
    logger.debug(f'start tcp server success! Listen port:{SERVER_PORT}')
    while True:
        tcp_client, client_address = tcp_server.accept()
        # 使用线程池防止攻击
        pool.submit(recv_msg, tcp_client, client_address)
        # t1 = threading.Thread(target=recv_msg, args=(tcp_client,client_address))
        # # 设置守护线程
        # t1.setDaemon(True)
        # t1.start()


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 8002
    uvicorn.run(app='main:app', host=HOST, port=PORT, reload=True, workers=1)
    # thd_server = multiprocessing.Process(target=server)
    # thd_tcp = multiprocessing.Process(target=tcpworker, args=(tcp_deque,))
    # thd_server.start()
    # thd_tcp.start()

    # thd_server.join()
    # thd_tcp.join()

