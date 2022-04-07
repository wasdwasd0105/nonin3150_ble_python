"""
BLE Nonin 3150 Python Communication
-------------
A python program can collect and save data for Nonin 3150
-------------
Requirements:
1. bleak: https://github.com/hbldh/bleak

Apr/1/2022
"""

import asyncio
import csv
import os
from bleak import BleakScanner, BleakClient
from datetime import datetime
import struct
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice

NONIN_SERVICE_UUID = '46a970e0-0d5f-11e2-8b5e-0002a5d5c51b'
PLETH_CHAR_UUID = 'ec0a883a-4d24-11e7-b114-b2f933d5fe66'
PULSE_OX_CHAR_UUID = '0aad7ea0-0d60-11e2-8e3c-0002a5d5c51b'

#NONIN_address = "11:22:33:44:55:66"
Nonin_Name = "Nonin3150_xxxxxxxxx" # enter the serial number here

curdir = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = os.path.join(curdir, '..', 'Data')

PLETH_FILE = 'pleth.csv'
PULSE_OX_FILE =  'pulse_ox.csv'


async def nonin_collecter():

    queue = asyncio.Queue()
    def find_uart_device(device: BLEDevice, adv: AdvertisementData):
        # This assumes that the device includes the UART service UUID in the
        # advertising data. This test may need to be adjusted depending on the
        # actual advertising data supplied by the device.
        if Nonin_Name in adv.local_name:
            queue.put_nowait(device)
            print(device)
    async with BleakScanner(detection_callback=find_uart_device):
        print("Scanning for a device: ", Nonin_Name)
        # this just gets the first device that was queued, then we stop scanning
        device: BLEDevice = await queue.get()

    def handle_pulse_rx(_: int, data: bytearray):
        time2 = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
        if os.path.exists(PULSE_OX_FILE):
            f1 = open(PULSE_OX_FILE, 'a')
        else:
            f1 = open(PULSE_OX_FILE, 'w')
        pulse_ox_writer = csv.writer(f1)
        output = struct.unpack('>b?bhhbh', data) # >b?b??hbh
        output = list(output)
        output.append(time2)
        print(output)
        pulse_ox_writer.writerow(output)
        f1.flush()

    def handle_pleth_rx(_: int, data: bytearray):
        time2 = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
        if os.path.exists(PLETH_FILE):
            f2 = open(PLETH_FILE, 'a')
        else:
            f2 = open(PLETH_FILE, 'w')
        pleth_writer = csv.writer(f2)
        print('writing pleth here')
        output = struct.unpack('>b{}h'.format('H'*25), data)
        output = list(output)
        output.append(time2)
        print(output)
        pleth_writer.writerow(output)
        f2.flush()

    #device = await BleakScanner.find_device_by_address(device_identifier = NONIN_address, timeout=20.0)
    print(device)
    
    async with BleakClient(device) as client:
        await client.start_notify(PLETH_CHAR_UUID, handle_pleth_rx)
        await client.start_notify(PULSE_OX_CHAR_UUID, handle_pulse_rx)
        while True:
            await asyncio.sleep(1.0)

# It is important to use asyncio.run() to get proper cleanup on KeyboardInterrupt.
# This was introduced in Python 3.7. If you need it in Python 3.6, you can copy
# it from https://github.com/python/cpython/blob/3.7/Lib/asyncio/runners.py

try:
    asyncio.run(nonin_collecter())
except asyncio.CancelledError:
    # task is cancelled on disconnect, so we ignore this error
    pass