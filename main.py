import deviceble



async def main():
    device = deviceble.DeviceBle()
    while True:
        try:
            connected = await device.connect()
            if connected:
                await device.listen()
        except Exception as e:
            print(e)