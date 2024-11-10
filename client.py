# client.py
import asyncio
import websockets
import random
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

    async def send_status_notification(self, connector_id, status):
        request = call.StatusNotificationPayload(
            connector_id=connector_id,
            error_code="NoError",
            status=status
        )
        response = await self.call(request)
        print(response)

async def simulate_charge_point(charge_point_id):
    async with websockets.connect(f'ws://localhost:9000/{charge_point_id}') as ws:
        charge_point = ChargePoint(charge_point_id, ws)
        await charge_point.start()
        await charge_point.send_boot_notification()
        
        while True:
            await asyncio.sleep(random.randint(5, 15))
            status = random.choice(["Available", "Occupied", "Faulted"])
            connector_id = random.randint(1, 2)
            await charge_point.send_status_notification(connector_id, status)

async def main():
    charge_point_ids = [f"CP_{i}" for i in range(1, 6)]
    tasks = [simulate_charge_point(cp_id) for cp_id in charge_point_ids]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())