# nonin3150_ble_python
a python program can receive, record and plot Nonin 3150's data wirelessly on BLE

Use BLEak https://github.com/hbldh/bleak to handle the ble connection.
Should work on Windows, MacOS and Linux. It depend on if bleak library support the OS.

## Usage:
1. enter you nonin device name on ble_nonin.py. Should be "Nonin3150_" + your serial number
2. run programs "python ./ble_nonin.py & python ./grapher_nonin.py"

<img width="635" alt="Screen Shot 2022-04-07 at 5 28 11 AM" src="https://user-images.githubusercontent.com/12875499/162198541-71db16a6-1fc0-44e5-9009-bdb745ffd6b6.png">
