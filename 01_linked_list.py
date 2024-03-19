class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj):
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

    def remove_obj(self):
        if self.head and not self.tail:
            self.head = None
        else:
            prev = self.tail.get_prev()
            prev.set_next(None)
            self.tail = prev

    def get_data(self):
        lst = []
        curr = self.head
        while curr:
            lst.append(curr.get_data())
            curr = curr.get_next()
        return lst


class ObjList:
    def __init__(self, data=None, nxt=None, prev=None):
        self.__next = nxt
        self.__prev = prev
        self.__data = data

    def set_next(self, obj):
        self.__next = obj

    def set_prev(self, obj):
        self.__prev = obj

    def get_next(self):
        return self.__next

    def get_prev(self):
        return self.__prev

    def set_data(self, data):
        self.__data = data

    def get_data(self):
        return self.__data
