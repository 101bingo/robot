from datetime import datetime
from logging import exception
from fastapi import FastAPI,WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import random
from loguru import logger
import uvicorn
import asyncio
import time

from router.api import api_router
from control.fish_run import cmd_deque,live_data_deque
from control.ws import manager


app = FastAPI()
# 入口添加api_router
app.include_router(api_router, prefix="/api")


origins = [
    'http://localhost'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         # data = await websocket.receive_text()
#         # await websocket.send_text(f"hello:{data}")
#         time.sleep(1)
#         oxygen = round(random.uniform(3.0,20.0),1)
#         temperature = round(random.uniform(20.0,30.0),1)
#         data_dict = {
#             'oxygen':oxygen,
#             'temperature':temperature
#         }
#         await websocket.send_json(data_dict)
#         if live_data_deque:
#             print(11111111111111)
#             msg = live_data_deque.popleft()
#             print('msg:', msg)
#             await websocket.send_json(data_dict)
#         else:
#             await asyncio.sleep(0.01)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            time.sleep(1)
            # data = await websocket.receive_text()
            oxygen = round(random.uniform(3.0,20.0),1)
            temperature = round(random.uniform(20.0,30.0),1)
            data_dict = {
                'oxygen':oxygen,
                'temperature':temperature
            }
            logger.info(str(data_dict))
            if manager.active_connections:
                await manager.broadcast(data_dict)
            if live_data_deque:
                print(11111111111111)
                msg = live_data_deque.popleft()
                print('msg:', msg)
                await websocket.send_json(data_dict)
            else:
                await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

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


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 8002
    uvicorn.run(app='main:app', host=HOST, port=PORT, reload=True, debug=True, workers=1)
