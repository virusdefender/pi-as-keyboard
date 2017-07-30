import string


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
            f.flush()


write_hid("abcdEDFR123490!@")