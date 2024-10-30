from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import requests
import asyncio
from typing import List


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients: List[WebSocket] = []

CURRENCY_API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

last_rates = {}

async def notify_clients(rate_changes):
    if clients:
        message = {"rate_changes": rate_changes}
        for client in clients:
            await client.send_json(message)

async def fetch_currency_rates():
    global last_rates
    while True:
        try:
            response = requests.get(CURRENCY_API_URL)
            data = response.json()
            current_rates = {item["CharCode"]: item["Value"] for item in data["Valute"].values()}

            rate_changes = current_rates if not last_rates else {
                code: value for code, value in current_rates.items() if last_rates.get(code) != value
            }

            if rate_changes:
                await notify_clients(rate_changes)

            last_rates = current_rates
        except Exception as e:
            print(f"Error fetching currency rates: {e}")

        await asyncio.sleep(10) 

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_currency_rates())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print(f"Client connected: {websocket.client}")

    await websocket.send_json({"rate_changes": last_rates})

    try:
        while True:
            await websocket.receive_text() 
    except WebSocketDisconnect:
        clients.remove(websocket)
        print(f"Client disconnected: {websocket.client}")

@app.get("/", response_class=HTMLResponse)
async def get():
    return FileResponse("index.html")
