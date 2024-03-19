class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


class Router:
    def __init__(self):
        self.servers = []
        self.buffer = []

    def link(self, server):
        self.servers.append(server)
        server.router = self

    def unlink(self, server):
        self.servers.remove(server)
        server.router = None

    def send_data(self):
        for data in self.buffer:
            for server in self.servers:
                if data.ip == server.ip:
                    server.buffer.append(data)
        self.buffer.clear()


class Server:
    COUNTER = 0

    @classmethod
    def counter(cls):
        cls.COUNTER += 1
        return cls.COUNTER

    def __init__(self):
        self.ip = self.counter()
        self.buffer = []
        self.router = None

    def get_ip(self):
        return self.ip

    def get_data(self):
        lst = self.buffer[:]
        self.buffer.clear()
        return lst

    def send_data(self, data):
        if self.router:
            self.router.buffer.append(data)

a = ('rer', 'fefe')
b=(1,2)
print({key: value for key, value in zip(a, b)})