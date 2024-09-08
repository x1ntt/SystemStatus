import time
import threading
import traceback

class Status():
    def __init__(self):
        self.nodes = {}
        self.lock = threading.Lock()
    
    def update_node(self, nodeinfo, ip):
        with self.lock:
            nodeinfo['ts'] = time.time()
            nodeinfo['ip'] = ip
            self.nodes[nodeinfo['ip']] = nodeinfo
    
    def getall_node(self):
        with self.lock:
            self.nodes = dict(filter(lambda item: time.time()-item[1]['ts']<3, self.nodes.items()))
            nodes = self.nodes.copy()
            return nodes


status = Status()
