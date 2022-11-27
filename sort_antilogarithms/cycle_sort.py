def _cycle_sort(arr):
    length = len(arr)

    repeatidxs = []
    for i in range(length):
        curridx = i
        nextidx = arr[curridx]
        while arr[nextidx] != nextidx:
            arr[curridx], arr[nextidx] = arr[nextidx], arr[curridx]
            nextidx = arr[curridx]
        if arr[i] != i:
            repeatidxs.append(i)

    # print(repeatidxs)
    for p in range(length):
        tmp = arr[p]
        i = p
        while i >= 1 and arr[i - 1] > tmp:
            arr[i] = [arr[i - 1]]
            i -= 1
        arr[i] = [tmp]
