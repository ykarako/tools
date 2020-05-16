import subprocess

DEVICE_LIST = [
    ("See3CAM", "2560:c120", 2),
    ("Pico Zense", "2d40:0101", 4),
    ("Soracom", "12d1:1506", 1),
    ("DX Hub", "0403:6014", 1),
    ("Mbed", "0d28:0204", 1),
    ("Line Cam", "0458:708c", 1),
]

result = subprocess.check_output("lsusb")
num_ok = 0
num_ng = 0

print("================== Confirm USB devices connection ===================")
for name, id, num in DEVICE_LIST:
    num_act = result.count(id)
    ok = num == num_act
    if ok:
        num_ok += 1
    else:
        num_ng += 1
    print("[{:16s}] ({}), expect num: {}, actual num: {} ----> {}".format(
        name, id, num, num_act, "OK" if ok else "NG"))
print("Total result -> OK: {}, NG: {}".format(num_ok, num_ng))
