import time

class Status():
    def __init__(self):
        self.nodes = {}
    
    def update_node(self, nodeinfo, ip):
        nodeinfo['ts'] = time.time()
        nodeinfo['ip'] = ip
        self.nodes[nodeinfo['ip']] = nodeinfo
    
    def getall_node(self):
        self.nodes = dict(filter(lambda item: time.time()-item[1]['ts']<3, self.nodes.items()))
        return self.nodes


status = Status()
