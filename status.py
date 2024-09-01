import time

class Status():
    def __init__(self):
        self.nodes = {}
    
    def clear_node(self):
        self.nodes = dict(filter(lambda item: time.time()-item[1]['ts']<3, self.nodes.items()))
    
    def update_node(self, nodeinfo):
        nodeinfo['ts'] = time.time()
        self.nodes[nodeinfo['ip']] = nodeinfo
    
    def getall_node(self):
        self.clear_node()
        return self.nodes


status = Status()