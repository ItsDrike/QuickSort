def partition(arr: list, start: int, end: int) -> int:
    # Set pivot as last element (for convenience)
    pivot_value = arr[end]
    pivot_index = start

    # Go through start-end elements and swap with pivot_index
    # whenever value is less than pivots value
    # after swap, increment the pivot_index
    for i in range(start, end):
        if arr[i] < pivot_value:
            arr[i], arr[pivot_index] = arr[pivot_index], arr[i]
            pivot_index += 1
    # Preform last swap to get the pivot in the middle
    arr[end], arr[pivot_index] = arr[pivot_index], arr[end]
    return pivot_index


def quick_sort(arr: list, start: int, end: int) -> None:
    # Stop when start reaches end (that section is now sorted)
    if start >= end:
        return

    # get pivot index (middle value, to which things are sorted)
    index = partition(arr, start, end)
    # Sort values in the 2 remaining sections (before and after pivot middle value)
    quick_sort(arr, start, index - 1)
    quick_sort(arr, index + 1, end)


if __name__ == "__main__":
    LIST = [9, 3, 4, 6, 5]

    quick_sort(LIST, 0, len(LIST) - 1)
    print(LIST)
