import typing as t


def remap(value: t.Union[int, float], from_range: t.Tuple[int, int], to_range: t.Tuple[int, int]) -> t.Union[int, float]:
    """Remap any given number within given range into another range."""
    old_range = from_range[1] - from_range[0]
    new_range = to_range[1] - to_range[0]

    new_value = (((value - from_range[0]) * new_range) / old_range) + to_range[0]
    return new_value


def list_remap(arr: t.List[t.Union[int, float]], range: t.Tuple[int, int]) -> t.List[t.Union[int, float]]:
    """Remap all values withing given list into another range."""
    original_range = (min(arr), max(arr))

    result = []
    for element in arr:
        new_value = remap(element, original_range, range)
        result.append(new_value)

    return result
