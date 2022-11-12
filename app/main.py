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
from control.login import *
from control.ws import manager

tcp_deque = deque()       # tcp消息队列
# tcp_deque = multiprocessing.Queue()       # tcp消息队列
IS_TCP_START = 0


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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        # await websocket.send_text(f"hello:{data}")
        # time.sleep(1)
        # oxygen = round(random.uniform(3.0,20.0),1)
        # temperature = round(random.uniform(20.0,30.0),1)
        # data_dict = {
        #     'oxygen':oxygen,
        #     'temperature':temperature
        # }
        # await websocket.send_json(data_dict)
        if live_data_deque:
            print(11111111111111)
            msg = live_data_deque.popleft()
            print('msg:', msg)
            data_dict = {
                'oxygen':msg[0]/10.0,
                'temperature':msg[1]/10.0
            }
            await websocket.send_json(data_dict)
        else:
            await asyncio.sleep(0.01)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             time.sleep(1)
#             # data = await websocket.receive_text()
#             oxygen = round(random.uniform(3.0,20.0),1)
#             temperature = round(random.uniform(20.0,30.0),1)
#             data_dict = {
#                 'oxygen':oxygen,
#                 'temperature':temperature
#             }
#             logger.info(str(data_dict))
#             if manager.active_connections:
#                 await manager.broadcast(data_dict)
#             if live_data_deque:
#                 print(11111111111111)
#                 msg = live_data_deque.popleft()
#                 print('msg:', msg)
#                 await websocket.send_json(data_dict)
#             else:
#                 await asyncio.sleep(0.01)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

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

@app.get('/startTcp')
def start_tcp_server():
    global IS_TCP_START,tcp_deque
    if IS_TCP_START:
        return {'res':0, 'msg':'tcp server is already started'}
    else:
        IS_TCP_START = 1
        thd_tcp = threading.Thread(target=tcpworker, args=(tcp_deque,))
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

def tcpworker(tcp_deque: deque):
    IP_ADDRESS = '42.193.138.254'
    SERVER_PORT = 6111
    tcp_server = socket(AF_INET, SOCK_STREAM)
    #设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    #绑定端口
    tcp_server.bind(('', SERVER_PORT))
    tcp_server.listen(4)
    logger.debug(f'start tcp server success! Listen port:{SERVER_PORT}')
    while True:
        tcp_client, client_address = tcp_server.accept()
        recv = tcp_client.recv(64)
        logger.debug(f'[{client_address}]->recv:{recv}')
        tcp_deque.append(recv)
        tcp_client.close()


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

