import time

def start_LED_monitoring():
    with open("/dev/hidg0","rb") as f:
        while True:
            data = f.read(1)
            a = ord(data)
            f.flush()
	    b = int("0x" + data.encode("hex"), 16)
            print(1 if b >=2 else 0, time.time())
start_LED_monitoring()
