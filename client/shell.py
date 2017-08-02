import time
import struct
import os


def write_led(led, value):
    fd = os.open("/dev/input/by-path/pci-0000:02:03.0-usb-0:2:1.0-event-kbd", os.O_WRONLY)
    now = time.time()
    sec = int(now)
    usec = int((now - sec) * 1.0E6)
    data = struct.pack('@llHHI', sec, usec, 0x11, led, value)
    os.write(fd, data)
    os.close(fd)


state_table = [[1, 2],
               [0, 3],
               [0, 3],
               [1, 2]]

last_state = 0


def write_data(data):
    global last_state
    for item in data:
        cur_value = int(item != "0")
        last_state = state_table[last_state][cur_value]
        print "data", item, "cur value", cur_value, "cur_state", last_state
        for i in range(2):
            print "write led", i, "value", int((last_state & (i + 1)) != 0)
            write_led(i, int((last_state & (i + 1)) != 0))


if __name__ == "__main__":
    import sys
    bin_data = "".join([bin(ord(item))[2:].zfill(8) for item in "".join(sys.argv[1:])])
    write_data(bin_data)
