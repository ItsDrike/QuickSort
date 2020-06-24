import typing as t
import pygame
import time
import sys
from contextlib import suppress


SIZE = WIDTH, HEIGHT = 500, 350

BLACK = 0, 0, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
WHITE = 255, 255, 255

MINIMUM_LINE_LENGTH = 50
SEPARATION = 8

TICK_RATE = 10

PIVOT_INDEXES = []
PROCESSING_INDEXES = []


def update_screen(screen: pygame.Surface, fps_clock: pygame.time.Clock, arr: t.List[int], no_tick=False) -> None:
    screen.fill(BLACK)
    draw_lines(screen, WHITE, RED, BLUE, arr)
    pygame.display.update()
    if not no_tick:
        fps_clock.tick(TICK_RATE)


def swap(arr: list, index1: int, index2: int):
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp


def partition(screen: pygame.Surface, fps_clock: pygame.time.Clock, arr: list, start: int, end: int) -> int:
    for i in range(start, end):
        PROCESSING_INDEXES.append(i)
        update_screen(screen, fps_clock, arr, no_tick=True)

    # Set pivot as last element (for convenience)
    pivot_value = arr[end]
    pivot_index = start

    PIVOT_INDEXES.append(pivot_index)
    update_screen(screen, fps_clock, arr)

    # Go through start-end elements and swap with pivot_index
    # whenever value is less than pivots value
    # after swap, increment the pivot_index
    for i in range(start, end):
        if arr[i] < pivot_value:
            swap(arr, i, pivot_index)
            PIVOT_INDEXES.remove(pivot_index)
            PROCESSING_INDEXES.remove(pivot_index)
            update_screen(screen, fps_clock, arr)
            pivot_index += 1
            PIVOT_INDEXES.append(pivot_index)
            update_screen(screen, fps_clock, arr)
    # Preform last swap to get the pivot in the middle
    swap(arr, end, pivot_index)

    for i in range(start, end):
        with suppress(ValueError):
            PROCESSING_INDEXES.remove(i)
        update_screen(screen, fps_clock, arr, no_tick=True)

    return pivot_index


def quick_sort(screen: pygame.Surface, fps_clock: pygame.time.Clock, arr: list, start: int, end: int) -> None:
    # Stop when start reaches end (that section is now sorted)
    if start >= end:
        return

    # get pivot index (middle value, to which things are sorted)
    index = partition(screen, fps_clock, arr, start, end)
    PIVOT_INDEXES.remove(index)
    update_screen(screen, fps_clock, arr)

    # Sort values in the 2 remaining sections (before and after pivot middle value)
    quick_sort(screen, fps_clock, arr, start, index - 1),
    quick_sort(screen, fps_clock, arr, index + 1, end)


def remap(value: t.Union[int, float], from_range: t.Tuple[int, int], to_range: t.Tuple[int, int]) -> t.Union[int, float]:
    """Remap any given number within given range into another range."""
    old_range = from_range[1] - from_range[0]
    new_range = to_range[1] - to_range[0]

    new_value = (((value - from_range[0]) * new_range) / old_range) + to_range[0]
    return new_value


def list_remap(LIST: t.List[t.Union[int, float]], range: t.Tuple[int, int]) -> t.List[t.Union[int, float]]:
    """Remap all values withing given list into another range."""
    original_range = (min(LIST), max(LIST))

    result = []
    for element in LIST:
        result.append(remap(element, original_range, range))

    return result


def draw_lines(
    screen: pygame.Surface,
    main_color: t.Tuple[int, int, int],
    pivot_color: t.Tuple[int, int, int],
    processing_color: t.Tuple[int, int, int],
    LIST: t.List[int],
) -> t.List[int]:
    LIST = list_remap(LIST, (0, HEIGHT - MINIMUM_LINE_LENGTH))
    lines = []
    for index, value in enumerate(LIST):
        # Start with 20 units gap, and draw lines with SEPARATION units separation on X
        x_pos = 20 + index * SEPARATION
        # Get height on Y axis
        y_pos = HEIGHT - value - MINIMUM_LINE_LENGTH
        if index in PIVOT_INDEXES:
            color = pivot_color
        elif index in PROCESSING_INDEXES:
            color = processing_color
        else:
            color = main_color

        # Draw the lines and add them into `lines` list
        line = pygame.draw.line(screen, color, (x_pos, HEIGHT), (x_pos, round(y_pos)))
        lines.append(line)

    return lines


def main_loop(screen: pygame.Surface, fps_clock: pygame.time.Clock, LIST: t.List[int]) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    quick_sort(screen, fps_clock, LIST, 0, len(LIST) - 1)

    update_screen(screen, fps_clock, LIST)

    time.sleep(3)


def pygame_start(LIST: t.List[int]) -> None:
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    fps_clock = pygame.time.Clock()

    # Don't start straight away
    time.sleep(8)

    main_loop(screen, fps_clock, LIST)


if __name__ == "__main__":
    LIST = [1, 5, 8, 3, 2, 9, 6, 10, 12, 11, 7, 13, 16, 14, 15]
    pygame_start(LIST)
