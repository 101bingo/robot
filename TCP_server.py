from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET,socket
from collections import deque
from datetime import datetime
import threading
import asyncio
from loguru import logger
import websocket
import requests
import json

msg_dequeue = deque()
live_data = deque()

# async def recv_cmd_ws(websocket):
#     while True:
#         recv_text = await websocket.recv()
#         if recv_text:
#             print('recv_text:', recv_text)
#             msg_dequeue.append(recv_text)

# async def ws_connected():
#     async with websockets.connect('ws://127.0.0.1:8082/sendcmd') as ws:
#         await recv_cmd_ws(ws)

# async def ws_live_data(msg):
#     async with websockets.connect('ws://127.0.0.1:8002/livedata') as ws:
#         await ws.send(msg)

def save_oxygen_data(oxygen, temperature):
    """ 保存溶氧数据到数据库，请求后端 """
    body={
        'oxygen':oxygen,
        'temperature':temperature
    }
    res = requests.post(url='http://localhost:8002/api/fish/addData',headers={'accept': 'application/json'},\
                        data=json.dumps(body))
    print('res:', res)

def send_live_data_to_background(oxygen, temperature):
    """ 同步实时数据到后台，方便手机端实时显示溶氧数据 """
    body = {
        'oxygen':oxygen,
        'temperature':temperature
    }
    res = requests.post(url='http://localhost:8002/api/fish/sendOxygen',headers={'accept': 'application/json'},\
                        data=json.dumps(body))
    print('res:', res)

def dispose_client_request(tcp_client, client_address):
    start_time = datetime.now()
    ws = websocket.WebSocket()
    ws.connect('ws://127.0.0.1:8002/livedata')
    #循环接受或发送数据
    while True:
        run_time = datetime.now()
        recv_data = tcp_client.recv(256)

        ws.ping()
        # ws_res = ws.recv_data_frame()
        ws_res = ws.recv_frame()
        logger.debug(f'recv_fram:{ws_res}')
        if ws_res[0] == 9:
            ws.pong()
        elif not ws_res.opcode == 10:
            ws.connect('ws://127.0.0.1:8002/livedata')
        #有消息处理
        if recv_data:
            res = [int(i) for i in recv_data]
            print('receve_data:', res)
            ws.send(str(res))
            print('websocket send success!')
            # oxygen = float(res[0])
            # temperature = float(res[1])
            # send_live_data_to_background(oxygen, temperature)
            # if run_time.minute-start_time.minute==1:
            #     start_time = run_time
            #     save_oxygen_data(oxygen, temperature)
        
        #发送后台命令
        if msg_dequeue:
            msg = msg_dequeue.popleft()
            tcp_client.send(msg)

def main_proc():
    IP_ADDRESS = '42.193.138.254'
    SERVER_PORT = 6222
    tcp_server = socket(AF_INET, SOCK_STREAM)
    #设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    #绑定端口
    tcp_server.bind(('', SERVER_PORT))
    tcp_server.listen(4)

    #循环等待客户端链接
    while True:
        tcp_client1, client_address = tcp_server.accept()
        print('connect_client:', client_address)
        print(tcp_client1)
        #创建多线程对象
        thd = threading.Thread(target=dispose_client_request, args=(tcp_client1, client_address))

        #设置守护线程
        thd.setDaemon(True)

        #启动子线程
        thd.start()

if __name__ == '__main__':
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    # asyncio.get_event_loop().run_until_complete(ws_connected())
    asyncio.get_event_loop().run_until_complete(main_proc())
    # main_proc()

    

