from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json

KEYBOARD = None
DEVICE = None


class SimpleEcho(WebSocket):
    def handleMessage(self):
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
                self.sendMessage(json.dumps({"index": data["index"], "status": status}))
                if DEVICE:
                    DEVICE.sendMessage(self.data)
            else:
                if KEYBOARD:
                    KEYBOARD.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")


server = SimpleWebSocketServer("", 8003, SimpleEcho)
server.serveforever()