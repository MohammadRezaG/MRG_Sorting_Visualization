def get_pivot(arr, left, right):
    mid = (left + right) // 2
    if arr[left] > arr[right]:
        arr[left], arr[right] = arr[right], arr[left]

    if arr[left] > arr[mid]:
        arr[left], arr[mid] = arr[mid], arr[left]

    if arr[mid] > arr[right]:
        arr[mid], arr[right] = arr[right], arr[mid]

    arr[mid], arr[right - 1] = arr[right - 1], arr[mid]

    return arr[right - 1]


def q_sort(arr, left, right):
    cutoff = 10
    if cutoff <= right - left:
        pivot = get_pivot(arr, left, right)
        low = left + 1
        high = right - 2
        while True:
            while arr[low] < pivot:
                low += 1
            while arr[high] > pivot:
                high -= 1
            if low < high:
                arr[low], arr[high] = arr[high], arr[low]
                low += 1
                high -= 1
            else:
                break
        arr[low], arr[right - 1] = arr[right - 1], arr[low]
        q_sort(arr, left, low - 1)
        q_sort(arr, low + 1, right)

    else:
        for p in range(left, right + 1):
            tmp = arr[p]
            i = p
            while i >= 1 and arr[i - 1] > tmp:
                arr[i] = arr[i - 1]
                i -= 1
                arr[i] = tmp


def quick_sort(arr):
    Length = len(arr)
    q_sort(arr, 0, Length - 1)
