import string
import json
import time
from websocket import create_connection


class HexStr(str):
    def __repr__(self):
        return "'" + ''.join('\\x{:02x}'.format(ord(ch)) for ch in self) + "'"
    __str__ = __repr__


# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
shift = "\x02"
no_shift = "\x00"
shift_number = "!@#$%^&*("
others_table = {"0": (no_shift, HexStr("\x27")),
                ")": (shift, HexStr("\x27")),
                "\n": (no_shift, HexStr("\x28")),
                "\t": (no_shift, HexStr("\x2b")),
                " ": (no_shift, HexStr("\x2c"))}


def letter_to_keycode(key):
    if key in string.ascii_uppercase:
        return shift, letter_to_keycode(key.lower())[1]
    elif key in string.ascii_lowercase:
        return no_shift, HexStr(chr(ord(key.lower()) - 93))
    elif key in "123456789":
        return no_shift, HexStr(chr(ord(key) - 19))
    elif key == "0":
        return no_shift, HexStr("\x27")
    elif key in shift_number:
        return shift, letter_to_keycode(str(shift_number.index(key) + 1))[1]
    else:
        return others_table[key]


def write_hid(s):
    with open("/dev/hidg0", "wb") as f:
        for item in s:
            s, k = letter_to_keycode(item)
            f.write(s + "\x00" + k + "\x00" * 5)
            f.write("\x00" * 8)
        f.write("\x00\x00" + others_table["\n"][1] + "\x00" * 5)
        f.writable("\x00" * 8)
        f.flush()

time.sleep(15)
ws = create_connection("ws://192.168.2.1:8083")
ws.send(json.dumps({"msg_type": "register", "client_type": "device"}))
while True:
    data = ws.recv()
    print(data)
    command = json.loads(data)
    if command["msg_type"] == "run_command":
        write_hid(command["command"])
        ws.send(json.dumps({"index": command["index"], "status": "done", "msg_type": "run_result"}).decode("utf-8"))