import unittest

from sorters import Sorters
from Visualizer import Visualizer, visualize, change_sorting_algorithm
import copy, time


class MyTestCase(unittest.TestCase):
    def test_something(self):
        sorters = Sorters()
        sorters_list = list(sorters.antilogarithms_dict.keys())

        n, min_val, max_val = 100, 5, 100
        r_arr = Visualizer.generate_starting_arr(n, min_val=min_val, max_val=max_val)
        c_arr = [1, 1, 1, 12, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 41000, 5, 65, 5, 5, 5, 5, 5, 5, 3, 5, 3, 1, 4, 5, 7, 7,
                 7, 7, 71434, 6]
        cs_arr = [1, 4, 4, 5, 5, 5, 1, 4, 7, 3, 2, 3, 2, 5, 12, 41000, 5, 3, 7, 7, 3, 65, 4, 5, 5, 5, 3, 3, 6, 71434, 7,
                  5, 4, 1, 3, 1]
        arr = r_arr + c_arr + cs_arr
        s_arr = copy.deepcopy(arr)
        s_arr.sort()
        for i, sorting_algorithm_name in enumerate(sorters_list):
            arr_copy = copy.deepcopy(arr)
            sorting_algorithm, sorting_algorithm_name, _ = change_sorting_algorithm(i, sorters.antilogarithms_dict)
            print(f'sorting using {sorting_algorithm_name} algorithm')
            sorting_algorithm(arr_copy)
            self.assertEqual(s_arr, arr_copy, 'sort algorithm {sorting_algorithm_name}')
            time.sleep(0.01)


if __name__ == '__main__':
    unittest.main()
