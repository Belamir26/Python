import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

asyncio.run(main())


import asyncio
from bleak import BleakClient

address = "CC:8D:A2:0D:44:2D"
MODEL_NBR_UUID = "00000001-0000-1000-8000-00805F9B34FB"

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))