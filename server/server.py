from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import logging

KEYBOARD = None
DEVICE = None


class SimpleEcho(WebSocket):
    def handleMessage(self):
        try:
            global KEYBOARD, DEVICE
            data = json.loads(self.data)
            print(data)
            if data["msg_type"] == "register":
                if data["client_type"] == "keyboard":
                    KEYBOARD = self
                else:
                    DEVICE = self
            else:
                if self == KEYBOARD:
                    if not DEVICE:
                        status = "no device"
                    else:
                        status = "running"
                    self.sendMessage(json.dumps({"index": data["index"], "status": status}).decode("utf-8"))
                    if DEVICE:
                        DEVICE.sendMessage(self.data.decode("utf-8"))
                else:
                    if KEYBOARD:
                        print("xxxxx")
                        KEYBOARD.sendMessage(self.data.decode("utf-8"))
        except Exception as e:
            logging.exception(e)

    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")


server = SimpleWebSocketServer("0.0.0.0", 8083, SimpleEcho)
server.serveforever()