from __future__ import annotations

from typing import Any


class LinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, value: ObjList) -> None:
        self.__head = value

    @property
    def tail(self):
        return self.__tail

    @tail.setter
    def tail(self, value: ObjList) -> None:
        self.__tail = value

    def add_obj(self, obj: ObjList) -> None:
        if not self.head:
            self.head = obj
        elif self.head and not self.tail:
            self.head.set_next(obj)
            obj.set_prev(self.head)
            self.tail = obj
        else:
            tail = self.tail
            tail.set_next(obj)
            obj.set_prev(tail)
            self.tail = obj

    def remove_obj(self) -> None:
        if self.head and not self.tail:
            self.head = None
        else:
            prev = self.tail.get_prev()
            prev.set_next(None)
            self.tail = prev

    def get_data(self) -> list:
        lst = []
        curr = self.head
        while curr:
            lst.append(curr.get_data())
            curr = curr.get_next()
        return lst


class ObjList:
    def __init__(self, data: Any = None, nxt: ObjList = None, prev: ObjList = None) -> None:
        self.__next = nxt
        self.__prev = prev
        self.__data = data

    def set_next(self, obj: ObjList | None) -> None:
        self.__next = obj

    def set_prev(self, obj: ObjList) -> None:
        self.__prev = obj

    def get_next(self) -> ObjList:
        return self.__next

    def get_prev(self) -> ObjList:
        return self.__prev

    def set_data(self, data: Any) -> None:
        self.__data = data

    def get_data(self) -> None:
        return self.__data
