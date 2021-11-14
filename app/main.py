from logging import debug
from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()

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

@app.get('/test')
async def test_fun():
    return {'msg':'靓仔，雷猴','code':'success'}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = websocket.receive_text()
        await websocket.send_text(f"hello:{data}")


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 6006
    uvicorn.run(app='main:app', host=HOST, port=PORT, reload=True, debug=True, workers=1)
