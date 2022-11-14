class Sorters:

    @staticmethod
    def bubble_sort(arr):
        length = len(arr)
        for i in range(length - 1, -1, -1):
            for j in range(0, i, 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
