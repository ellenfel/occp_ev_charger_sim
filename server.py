#pip install websockets ocpp

# server.py
import asyncio
import websockets
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result

class ChargePoint(cp):
    @on('BootNotification')
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        return call_result.BootNotificationPayload(
            current_time='2023-01-01T00:00:00Z',
            interval=10,
            status='Accepted'
        )

async def on_connect(websocket, path):
    charge_point_id = path.strip('/')
    charge_point = ChargePoint(charge_point_id, websocket)
    await charge_point.start()

async def main():
    server = await websockets.serve(on_connect, 'localhost', 9000)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())