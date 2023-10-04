import pygame
import random
import math
from Data_arr import DataArr
import sorters, color_constants
import threading

WIDTH, HEIGHT = 1200, 900


class Visualizer:
    BLACK = 0, 0, 0
    DARK_GRAY = color_constants.GRAY10
    LITE_GRAY = color_constants.GRAY
    WHITE = color_constants.WHITE
    GREEN = color_constants.GREEN1
    RED = color_constants.RED1
    BLUE = color_constants.AQUA
    PURPLE = color_constants.PURPLE
    PINK = color_constants.DEEPPINK3
    BACKGROUND_COLOR = DARK_GRAY

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    SIDE_PAD = 50
    TOP_PAD = 150

    def reset(self):
        self.arr = DataArr(self.arr_gen(self.n_arr, self.min_val, self.max_val), draw_info=self)

        self.block_width = round((self.width - self.SIDE_PAD) / len(self.arr))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

    def init(self):
        pygame.init()
        self.SMALL_FONT = pygame.font.SysFont('comicsans', 10)
        self.FONT = pygame.font.SysFont('comicsans', 20)
        self.LARGE_FONT = pygame.font.SysFont('comicsans', 30)
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualization")

    def __init__(self, width, height, init=False, arr_gen=None, n_arr=50, min_val=5, max_val=100, mt_flag=True):
        self.width = width
        self.height = height

        if init:
            self.init()

        self.n_arr = n_arr
        self.min_val = min_val
        self.max_val = max_val

        if arr_gen is None:
            self.arr_gen = self.generate_starting_arr
        else:
            self.arr_gen = arr_gen

        self.mt_flag = mt_flag

        self.color_positions = {}
        self.black_bg = True
        self.bg_side_margin = 20
        self.bg_top_margin = 20

        self.sorting_algorithm_name = 'None'
        self.sorting_algorithm = 'None'
        self.reset()

    def draw_bars(self):
        arr = self.arr._arr

        if self.black_bg:
            clear_rect = (self.SIDE_PAD // 2 - self.bg_side_margin, self.TOP_PAD - self.bg_top_margin,
                          self.width - self.SIDE_PAD + (self.bg_side_margin * 2),
                          self.height - self.TOP_PAD + (self.bg_top_margin * 2))
            pygame.draw.rect(self.window,
                             self.BLACK, clear_rect)

        for i, val in enumerate(arr):
            x = self.start_x + i * self.block_width
            y = (self.height - (val - self.min_val) * self.block_height) - 1

            color = self.GRADIENTS[i % 3]

            if i in self.color_positions:
                color = self.color_positions[i]

            pygame.draw.rect(self.window, color,
                             (x, y, self.block_width, self.height))

        pygame.display.update()

    def draw(self):
        self.window.fill(self.BACKGROUND_COLOR)

        lbl_algorithm = self.FONT.render(
            f"algorithm: {self.sorting_algorithm_name}", 1, self.BLUE)
        self.window.blit(lbl_algorithm, (2, 5))

        lbl_arr_accesses_time = self.FONT.render(
            f"array accesses time: {self.arr.arr_accesses_time}", 1, self.LITE_GRAY)
        self.window.blit(lbl_arr_accesses_time, (2, 80))

        lbl_arr_accesses_time = self.FONT.render(
            f"array accesses count: {self.arr.arr_accesses}", 1, self.LITE_GRAY)
        self.window.blit(lbl_arr_accesses_time, (350, 80))

        lbl_arr_writes_time = self.FONT.render(
            f"array writes count: {self.arr.arr_writes}", 1, self.LITE_GRAY)
        self.window.blit(lbl_arr_writes_time, (350, 60))

        lbl_arr_accesses_time = self.FONT.render(
            f"multithreading: {self.mt_flag}", 1, self.LITE_GRAY)
        self.window.blit(lbl_arr_accesses_time, (2, 60))

        lbl_arr_accesses_time = self.FONT.render(
            f"n_arr: {self.n_arr}", 1, self.LITE_GRAY)
        self.window.blit(lbl_arr_accesses_time, (2, 40))

        lbl_reset = self.FONT.render(
            f"for reset press R", 1, self.BLUE)
        self.window.blit(lbl_reset, (self.width - lbl_reset.get_size()[0] - 10, 80))

        self.draw_bars()

        pygame.display.update()

    @staticmethod
    def generate_starting_arr(size, min_val, max_val):
        return [random.randint(min_val, max_val) for i in range(size)]


def change_sorting_algorithm(i, al_dict: dict):
    al_dict_keys = list(al_dict.keys())
    if i >= len(al_dict_keys):
        i = 0
    elif i < 0:
        i = len(al_dict_keys) - 1
    al_name = al_dict_keys[i]
    return al_dict[al_name], al_name, i


def run_sorting_algorithm(sorting_algorithm, arr, sorting_lock=None, mt=False, mt_name='sorting_algorithm'):
    if mt:
        def thread(funk, a, lock: threading.Lock):
            lock.acquire()
            funk(a)
            lock.release()

        if sorting_lock:
            thread = threading.Thread(target=thread, name=mt_name,
                                      kwargs={'funk': sorting_algorithm, 'a': arr, 'lock': sorting_lock})
            thread.start()
        else:
            raise ValueError('sorting_lock cant be None')

    else:
        sorting_algorithm(arr)
        return None


def visualize(draw_info):
    if not pygame.get_init():
        draw_info.init()
    run = True
    clock = pygame.time.Clock()
    # arr = [0,0,0,0,1,1,1,120,2,2,1,1,1,1,10,0,0,0,0]

    draw_info.arr.arr_accesses_time = 0.09
    i = 0
    sorter = sorters.Sorters()
    draw_info.sorting_algorithm, draw_info.sorting_algorithm_name, i = change_sorting_algorithm(i,
                                                                                                sorter.antilogarithms_dict)

    sorting_lock = threading.Lock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE] and sorting_lock.locked() is False:

                    run_sorting_algorithm(draw_info.sorting_algorithm, draw_info.arr,
                                          sorting_lock=sorting_lock,
                                          mt=draw_info.mt_flag,
                                          mt_name='sorting_algorithm')

                elif keys[pygame.K_SPACE] and sorting_lock.locked() is True and not draw_info.arr.arr_lock.locked():
                    draw_info.arr.arr_lock.acquire()

                elif keys[pygame.K_SPACE] and sorting_lock.locked() is True and draw_info.arr.arr_lock.locked():
                    draw_info.arr.arr_lock.release()

                elif (keys[pygame.K_r] and sorting_lock.locked() is False) or \
                        (keys[pygame.K_r] and draw_info.arr.arr_lock.locked()):
                    draw_info.reset()

                # change arr_accesses_time t key
                elif keys[pygame.K_t] and keys[pygame.K_UP]:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        draw_info.arr.arr_accesses_time += 0.001
                    else:
                        draw_info.arr.arr_accesses_time += 0.01
                elif keys[pygame.K_t] and keys[pygame.K_DOWN]:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        draw_info.arr.arr_accesses_time -= 0.001
                    else:
                        draw_info.arr.arr_accesses_time -= 0.01

                # prevent changes when sorting_lock.locked() is True
                elif sorting_lock.locked():
                    #print('cant changes algoritm n_arr multithreading when running')
                    continue

                # change sorting_algorithm a key
                elif keys[pygame.K_a] and keys[pygame.K_UP]:
                    i += 1
                    sorting_algorithm, draw_info.sorting_algorithm_name, i = change_sorting_algorithm(i,
                                                                                                      sorter.antilogarithms_dict)
                elif keys[pygame.K_a] and keys[pygame.K_DOWN]:
                    i -= 1
                    sorting_algorithm, draw_info.sorting_algorithm_name, i = change_sorting_algorithm(i,
                                                                                                      sorter.antilogarithms_dict)

                # change n_arr n key
                elif keys[pygame.K_n] and keys[pygame.K_UP]:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        draw_info.n_arr += 10
                    else:
                        draw_info.n_arr += 1

                elif keys[pygame.K_n] and keys[pygame.K_DOWN]:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        draw_info.n_arr -= 10
                    else:
                        draw_info.n_arr -= 1

                # change mt_flag m key
                elif keys[pygame.K_m]:
                    if draw_info.mt_flag:
                        draw_info.mt_flag = False
                    else:
                        draw_info.mt_flag = True

        draw_info.draw()

    pygame.quit()


if __name__ == "__main__":
    draw_info = Visualizer(WIDTH, HEIGHT, init=True)
    visualize(draw_info)
