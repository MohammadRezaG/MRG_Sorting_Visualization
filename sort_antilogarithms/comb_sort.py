def comb_sort(arr):
    length = len(arr)
    D = int(length / 1.3)

    while D:
        for i in range(length):
            for j in range(i + D, length, D):
                if arr[j - D] > arr[j]:
                    arr[j - D], arr[j] = arr[j], arr[j - D]
        D = int(D / 1.3)
