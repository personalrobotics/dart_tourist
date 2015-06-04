from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                                    WebSocketServerFactory

import json, sys
from dart_tourist import SkeletonVisitor

g_dart_state = "{}"

class DartServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        global g_dart_state

        # ignore actual message content, just send back 
        # dart state
        self.sendMessage(g_dart_state, False)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

def set_dart_state(newstate):
    global g_dart_state
    g_dart_state = newstate

# builds up a python data structure
class JSONVisitor:
    def __init__(self):
        self.data = {}
        self.stack = deque()
        self.stack.append(self.data)

    def append(self, propname, propval):
        self.stack[-1][propname] = propval

    def pose4q3t(self, qx, qy, qz, qw, tx, ty, tz):
        self.append("rot", (qx, qy, qz, qw))
        self.append("trans", (tx, ty, tz))

    def scale3(self, sx, sy, sz):
        self.append("scale", (sx, sy, sz))

    def enter_mesh(self, meshname):
        curthing = {"filename": meshname}
        self.stack[-1]["nmeshes"] += 1
        self.stack[-1]["mesh.{}".format(self.stack[-1]["nmeshes"])] = curthing
        self.stack.append(curthing)

    def enter_body(self, bodyname):
        curthing = {"nmeshes": 0}
        self.stack[-1]["body." + bodyname] = curthing
        self.stack.append(curthing)

    def enter_skeleton(self, skelname):
        curthing = {}
        self.stack[-1]["skeleton." + skelname] = curthing
        self.stack.append(curthing)

    def leave(self):
        self.stack.pop()

    def toJSON(self, pretty=False):
        if not pretty:
            return json.dumps(self.data)
        else:
            return json.dumps(self.data, indent=1)

def update_skeleton(skel):
    visitor = JSONVisitor()
    skeletor = SkeletonVisitor("Skeletor")
    skeletor.visit_skeleton(skel, visitor)
    set_dart_state(visitor.message)
    return visitor.message

def server_thread_main():
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
    factory.protocol = DartServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run(installSignalHandlers=0)

def start_server_this_thread():
    server_thread_main()

def start_server():
    from threading import Thread

    ret = Thread(target=server_thread_main)
    ret.start()
    return ret

