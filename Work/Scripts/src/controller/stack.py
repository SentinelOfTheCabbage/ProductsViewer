class Stack:

    _list = []

    def __init__(self, capacity):
        if capacity <= 0:
            raise Exception("Capacity can't be negative or zero")
        self.capacity = capacity
        self.pos = -1

    def add(self, obj):
        if self.pos < self.capacity - 1:
            self.pos += 1
            self._list = self._list[:self.pos]
        else:
            self._list = self._list[1:]
        self._list.append(obj)

    def pop(self):
        return self._list.pop(-1)

    def clear(self):
        self._list.clear()
        self.pos = -1

    def prev(self):
        if self.pos > 0:
            self.pos -= 1
            return self._list[self.pos]

    def next(self):
        if self.pos < len(self._list) - 1:
            self.pos += 1
            return self._list[self.pos]

    def __str__(self):
        return str(self._list)
