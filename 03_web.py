from __future__ import annotations
from typing import Any


class Data:
    def __init__(self, data: Any, ip: int) -> None:
        self.__data = data
        self.ip = ip

    @property
    def ip(self) -> int:
        return self.__ip

    @ip.setter
    def ip(self, value) -> None:
        if isinstance(value, int):
            self.__ip = value
        else:
            raise TypeError('ip должен быть целым числом')

    @property
    def data(self) -> Any:
        return self.__data


class Router:
    def __init__(self) -> None:
        self.__servers = []
        self.__buffer = []

    @property
    def servers(self) -> list:
        return self.__servers

    @property
    def buffer(self) -> list:
        return self.__buffer

    def link(self, server: Server) -> None:
        self.servers.append(server)
        server.router = self

    def unlink(self, server: Server) -> None:
        self.servers.remove(server)
        server.router = None

    def send_data(self) -> None:
        for data in self.buffer:
            for server in self.servers:
                if data.ip == server.get_ip():
                    server.buffer.append(data)
        self.buffer.clear()


class Server:
    COUNTER = 0

    @classmethod
    def counter(cls) -> int:
        cls.COUNTER += 1
        return cls.COUNTER

    def __init__(self) -> None:
        self.__ip = self.counter()
        self.__buffer = []
        self.router = None

    @property
    def buffer(self) -> list:
        return self.__buffer

    @property
    def router(self) -> None | Router:
        return self.__router

    @router.setter
    def router(self, value) -> None:
        self.__router = value

    def get_ip(self) -> int:
        return self.__ip

    def get_data(self) -> list:
        lst = self.buffer[:]
        self.buffer.clear()
        return lst

    def send_data(self, data: Any) -> None:
        if self.router:
            self.router.buffer.append(data)
