# from Data_arr import DataArr
import os, types

try:
    import sort_antilogarithms
except ModuleNotFoundError:
    os.mkdir('sort_antilogarithms')
    homedir = os.path.dirname(__file__)
    filepath = os.path.join(homedir + r'\sort_antilogarithms', '__init__.py')
    with open(filepath, "w") as file:
        file.write(
            '''import os
            for module in os.listdir(os.path.dirname(__file__)):
                if module == '__init__.py' or module[-3:] != '.py':
                    continue
                __import__(f'sort_antilogarithms.{module[:-3]}', locals(), globals())
            del module
            '''
        )
    import sort_antilogarithms


class Sorters:
    def __init__(self):
        self.antilogarithms_dict = Sorters.get_antilogarithms_list(self)
        self.antilogarithms_dict.update(self._get_antilogarithms_list_from_module(sort_antilogarithms))

    @staticmethod
    def _get_antilogarithms_list_from_module(papa_module):
        """

        :rtype: dict
        """
        antilogarithms_dict = {}
        for module_name in papa_module.__dir__():
            if 'sort' in module_name and (not '__' in module_name):
                module = getattr(papa_module, module_name)
                if isinstance(module, types.FunctionType):
                    antilogarithms_dict[module_name] = module
                else:
                    antilogarithms_dict.update(Sorters._get_antilogarithms_list_from_module(module))
        return antilogarithms_dict

    @staticmethod
    def get_antilogarithms_list(sorters):
        antilogarithms_dict = {}
        for al_name in sorters.__dir__():
            if 'sort' in al_name:
                antilogarithms_dict[al_name] = getattr(sorters, al_name)
        return antilogarithms_dict

    @staticmethod
    def bubble_sort(arr):
        length = len(arr)
        for i in range(length - 1, -1, -1):
            for j in range(0, i, 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

    @staticmethod
    def selection_sort(arr):
        # Traverse through all array elements
        for i in range(len(arr)):

            # Find the minimum element in remaining
            # unsorted array
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[min_idx] > arr[j]:
                    min_idx = j

            # Swap the found minimum element with
            # the first element
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    @staticmethod
    def insertion_sort(arr):

        # Traverse through 1 to len(arr)
        for i in range(1, len(arr)):

            key = arr[i]

            # Move elements of arr[0..i-1], that are
            # greater than key, to one position ahead
            # of their current position
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    @staticmethod
    def merge_sort(arr):
        if len(arr) > 1:

            # Finding the mid of the array
            mid = len(arr) // 2

            # Dividing the array elements
            L = arr[:mid]

            # into 2 halves
            R = arr[mid:]

            # Sorting the first half
            Sorters.merge_sort(L)

            # Sorting the second half
            Sorters.merge_sort(R)

            i = j = k = 0

            # Copy data to temp arrays L[] and R[]
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            # Checking if any element was left
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
