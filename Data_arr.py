import random
import time
from threading import Lock


class DataArr:

    def __init__(self, arr, draw_info=None, arr_accesses_time=0):
        self._arr = arr
        self.arr_color = {}
        self.draw_info = draw_info
        self.auto_color = True
        self.arr_accesses = 0
        self.arr_writes = 0
        self.first_accessed_idx = None
        self.last_accessed_idx = None
        self.first_accessed_status = False
        self._arr_accesses_time = arr_accesses_time
        self.arr_lock = Lock()

    def _set_accessed_color(self, i):
        self.arr_color = {}
        if self.first_accessed_idx:
            self.arr_color[self.first_accessed_idx] = self.draw_info.PURPLE

        if not self.first_accessed_status:
            self.arr_color[i] = self.draw_info.PURPLE
            self.first_accessed_idx = i
            self.first_accessed_status = True
        else:
            self.arr_color[i] = self.draw_info.PINK

        self.last_accessed_idx = i

    def reset_first_accessed_status(self):
        if self.first_accessed_status:
            self.arr_color = {}
        self.first_accessed_status = False
        self.first_accessed_idx = None

    def _set_accessed(self, key, mode='get'):
        if not self.auto_color:
            return

        if mode == 'set':
            self.reset_first_accessed_status()

        if type(key) == int:
            self._set_accessed_color(key)

        elif type(key) == tuple:
            for i in key:
                self._set_accessed_color(i)

        elif type(key) == slice:
            for i in range(key.start, key.stop, key.step):
                self._set_accessed_color(i)

        if self.draw_info is not None:
            self.draw_info.draw_bars()

        if self._arr_accesses_time != 0:
            time.sleep(self._arr_accesses_time)
        if self.arr_lock.locked():
            self.arr_lock.acquire()
            self.arr_lock.release()

        self.draw_info.color_positions = self.arr_color

    @property  # getter
    def arr(self):
        self.arr_accesses += 1
        if self._arr_accesses_time != 0:
            time.sleep(self._arr_accesses_time)
        return self._arr

    @arr.setter  # setter
    def arr(self, val):
        self.arr_writes += len(val)
        self._arr = val

    @property  # getter
    def arr_accesses_time(self):
        return self._arr_accesses_time

    @arr_accesses_time.setter  # setter
    def arr_accesses_time(self, val):
        if val < 0:
            val = 0
            print(ValueError("arr_accesses_time cant be less than 0"))
        self._arr_accesses_time = val

    def __len__(self):
        return len(self.arr)

    def __getitem__(self, key):
        if self.draw_info is not None:
            self._set_accessed(key, 'get')
        return self.arr[key]

    def __setitem__(self, key, value):
        if self.draw_info is not None:
            self._set_accessed(key, 'set')
        self.arr_writes += 1
        self.arr[key] = value

    def __delitem__(self, key):
        if self.draw_info is not None:
            self._set_accessed(key, 'set')
        del self.arr[key]

    def __iter__(self):
        return iter(self.arr)

    def __reversed__(self):
        return reversed(self.arr)

    def __str__(self):
        return str(self.arr)

    def __repr__(self):
        return self.arr.__repr__()
