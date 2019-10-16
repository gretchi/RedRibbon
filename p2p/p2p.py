

class P2PNetwork(object):
    def __init__(self):
        self._peer_list = []

    def regist_peer(self, host, port):
        peer_host = None
        peer_port = None
        is_use_turn = False
