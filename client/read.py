def start_LED_monitoring():
    s = "0b"
    with open("/dev/hidg0", "rb") as f:
        while True:
            data = f.read(1)
            f.flush()
            b = int("0x" + data.encode("hex"), 16)
            s += "1" if b >= 2 else "0"
            if len(s) == 10:
                print(chr(int(s, 2)))
                s = "0b"


start_LED_monitoring()
