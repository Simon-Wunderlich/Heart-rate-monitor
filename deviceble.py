import asyncio

from bleak import BleakScanner, BleakClient
import requests

class DeviceBle:
    def __init__(self):
        self.device = None
        self.client = None
        self.uuid_heart_rate_measurement_characteristic = '00002a37-0000-1000-8000-00805f9b34fb'

    async def discover(self):
        devices = await BleakScanner.discover(5.0, return_adv=True)
        for device in devices:
            advertisement_data = devices[device][1]
            if advertisement_data.local_name == "H1_70068":
                if advertisement_data.rssi > -90:
                    self.device = devices[device]
                    return device
        return None

    async def connect(self):
        address = await self.discover()
        if address is not None:
            try:
                print("Found device at address: %s" % address)
                print("Attempting to connect...")
                self.client = BleakClient(address)
                await self.client.connect()
                print("Connected!")
                return True
            except:
                print("Failed to connect")
            return False

    async def listen(self):
        await self.client.start_notify(self.uuid_heart_rate_measurement_characteristic, self.notify)
        print("Subscribed! Waiting for data...")
        while self.client.is_connected:
            await asyncio.sleep(10)

    def notify(self, characteristic, data):
        url = "http://192.168.1.102:5000"
        try:
            requests.post(url, data=str(int(data.hex(), 16)), headers={'Content-Type': 'text/plain'})
        except:
            print("Host not found")