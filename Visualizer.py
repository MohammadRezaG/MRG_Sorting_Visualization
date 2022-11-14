import pygame
import random
import math
from Data_arr import DataArr
import sorters

pygame.init()

WIDTH, HEIGHT = 1200, 900


class Visualizer:
    BLACK = 0, 0, 0
    DARK_GRAY = 50, 50, 50
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = DARK_GRAY

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 50
    TOP_PAD = 150

    def __init__(self, width, height, arr):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")

        self.arr = DataArr(arr, draw_info=self)
        self.min_val = min(arr)
        self.max_val = max(arr)

        self.color_positions = {}
        self.black_bg = True
        self.bg_side_margin = 20
        self.bg_top_margin = 20

        self.block_width = round((self.width - self.SIDE_PAD) / len(arr))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

    def draw_bars(self, ):
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

        self.draw_bars()

        pygame.display.update()

    @staticmethod
    def generate_starting_arr(size, min_val, max_val):
        return [random.randint(min_val, max_val) for i in range(size)]


def visualize(width, height):
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 5
    max_val = 100

    arr = Visualizer.generate_starting_arr(n, min_val, max_val)
    #arr = [0,0,0,0,1,1,1,120,2,2,1,1,1,1,10,0,0,0,0]
    draw_info = Visualizer(width, height, arr)
    draw_info.arr.arr_accesses_time = 0.09

    sorting = False
    ascending = True

    sorting_algorithm = sorters.Sorters.bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    print("t")
                elif event.key == pygame.K_SPACE and sorting is False:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info.arr)

        draw_info.draw()

    pygame.quit()


if __name__ == "__main__":
    visualize(WIDTH, HEIGHT)
