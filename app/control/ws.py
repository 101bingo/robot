
from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from loguru import logger

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        websocket.close()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        logger.debug(f'connect_dict:{self.active_connections}')
        for connection in self.active_connections[:]:
            # await connection.send_text(message)
            try:
                logger.info(f'connect:{connection}')
                logger.warning(f'app_status:{connection.application_state}')
                logger.debug(str(message))
                await connection.send_json(message)
            except Exception as e:
                logger.error(str(e))
                self.active_connections.remove(connection)
                # connection.close()

manager = ConnectionManager()