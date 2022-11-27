from datetime import datetime
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET,socket
from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import random
from loguru import logger
import uvicorn
import asyncio
import time
import threading
import multiprocessing
from collections import deque

from router.api import api_router
from control.fish_run import cmd_deque,live_data_deque
from models.fish_model import add_oxygen_data_per_minute
from control.login import *
from control.ws import manager
from scheduler.write_mysql_job import init_scheduler
from control.weixin import send_msg_by_temple

# logger.add('/var/log/robot/service.log', rotation='50 MB')
logger.add(r'F:\WORK\code\debug\service.log', rotation='50 MB')
tcp_deque = deque()       # tcp消息队列
tcp_deque_backup = deque()       # tcp消息队列备份
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

@app.on_event('startup')
def init_scheduler_before():
    """ 初始化定时任务 """
    logger.debug('start init scheduler')
    init_scheduler(tcp_deque_backup)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    data_to_mysql = {}
    msg_key = ['date_time', 'temper', 'oxygen_perc', 'oxygen', 'count_time','is_ready_flag']
    while True:
        if tcp_deque:
            msg = tcp_deque.popleft()
            data_dict = dict(zip(msg_key, msg))
            date_time = datetime.strptime(data_dict['date_time'], '%Y-%m-%d %H:%M:%S')
            data_to_mysql['date_time'] = date_time
            data_to_mysql['temper'] = data_dict['temper']
            data_to_mysql['oxygen'] = data_dict['oxygen']
            data_to_mysql['oxygen_perc'] = data_dict['oxygen_perc']
            await manager.broadcast(data_dict)
        else:
            await asyncio.sleep(0.01)

@app.websocket("/sendcmd")
async def websocket_send(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            if cmd_deque:
                cmd = cmd_deque.popleft()
                await websocket.send_text(cmd)
                data = await websocket.receive_text()
    except Exception as e:
        await websocket.close()

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
                continue
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
    IP_ADDRESS = '42.193.138.254'
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
        t1 = threading.Thread(target=recv_msg, args=(tcp_client,client_address))
        # 设置守护线程
        t1.setDaemon(True)
        t1.start()


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 8002
    uvicorn.run(app='main:app', host=HOST, port=PORT, reload=True, debug=True, workers=1)
    # thd_server = multiprocessing.Process(target=server)
    # thd_tcp = multiprocessing.Process(target=tcpworker, args=(tcp_deque,))
    # thd_server.start()
    # thd_tcp.start()

    # thd_server.join()
    # thd_tcp.join()

