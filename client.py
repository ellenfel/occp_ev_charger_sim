# client.py
import asyncio
import websockets
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="EV Charger Model",
            charge_point_vendor="EV Charger Vendor"
        )
        response = await self.call(request)
        print(response)

async def main():
    async with websockets.connect('ws://localhost:9000/CP_1') as ws:
        charge_point = ChargePoint('CP_1', ws)
        await charge_point.start()
        await charge_point.send_boot_notification()

if __name__ == '__main__':
    asyncio.run(main())