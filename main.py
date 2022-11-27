from Visualizer import Visualizer, visualize, change_sorting_algorithm
import Data_arr
from sorters import Sorters
import pygame
from consolemenu import ConsoleMenu, SelectionMenu, items
from consolemenu.items import FunctionItem, SubmenuItem, CommandItem
from consolemenu.console_menu import ExitItem


class MrgExitItem(ExitItem):
    def __init__(self):
        super().__init__()

    def get_return(self):
        return 'EXIT'


def change_W_H():
    W = input("WIDTH =:")
    H = input("HEIGHT =:")
    if W.isnumeric():
        if H.isnumeric():
            return H, W
        else:
            H = 900
    else:
        W = 1600
    return Visualizer(W, H)


def sort(sorters, draw_info:Visualizer):
    stop = False
    arr = []
    while not stop:
        in_s = input('input an aray exp: 1,2,3,4 or put rnd for random generated arr default is (rnd)\n')
        if in_s == 'rnd' or in_s == '':
            in_s = input(
            'input number of val [n] min value [min_val] max value [max_val] in this format ( n min_val max_val ) default is (100 5 100) )\n'
            )
            if in_s != '':
                n, min_val, max_val = map(int, in_s.split(' '))
            else:
                n, min_val, max_val = 100, 5, 100

            arr = Visualizer.generate_starting_arr(n, min_val=min_val, max_val=max_val)
            stop = True
        elif ',' in in_s:
            for s in in_s.split(','):
                if s.isnumeric():
                    arr.append(float(s))
            stop = True


    sorters_inx = SelectionMenu.get_selection(sorters_list)
    d_arr = Data_arr.DataArr(arr=arr)
    sorting_algorithm, sorting_algorithm_name, _ = change_sorting_algorithm(sorters_inx, sorters.antilogarithms_dict)

    print(f'sorting using {sorting_algorithm_name} algorithm')
    print(f'before sorting \n arr => {str(d_arr)}')
    sorting_algorithm(d_arr)
    print(f'after sorting \n arr => {d_arr}')


if __name__ == "__main__":
    WIDTH, HEIGHT = 1200, 900
    draw_info = Visualizer(WIDTH, HEIGHT)
    sorters = Sorters()
    sorters_list = list(sorters.antilogarithms_dict.keys())
    stop = False

    while not stop:
        menu = ConsoleMenu("Welcome to sorting Visualizer")
        menu.exit_item = MrgExitItem()

        settings = ConsoleMenu("settings")
        settings_item = SubmenuItem("go to settings", settings, menu=menu)
        change_W_H_item = FunctionItem("change WIDTH HEIGHT", change_W_H, should_exit=True)
        settings.append_item(change_W_H_item)

        visualize_item = FunctionItem("visualize", visualize, [draw_info])
        do_some_sort_item = FunctionItem("sort", sort, [sorters, draw_info])

        menu.append_item(do_some_sort_item)
        menu.append_item(visualize_item)

        menu.append_item(settings_item)
        # menu.show_exit_option = 0

        menu.show()
        draw_info = change_W_H_item.get_return()

        if menu.exit_item.get_return() is 'EXIT':
            stop = True
