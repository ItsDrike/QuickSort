import sys
import time
from collections import defaultdict

import pygame

from util import list_remap


class Colors:
    """This class is only used to store colors."""
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 233, 255
    YELLOW = 255, 242, 0
    ORANGE = 255, 121, 0  # Merge of RED and YELLOW


ARRAY = [12, 58, 21, 13, 18, 42, 35, 49, 10, 3, 50, 28, 55, 4, 8, 9, 24, 49]
STATES = defaultdict(lambda: Colors.WHITE)


class QuickSort:
    """This class stores functions regarding the Quick Sort algorithm."""
    def __init__(self, game: "Game") -> None:
        self.game = game

    def partition(self, start: int, end: int) -> int:
        """
        Change the array in a way so that the last element (pivot)
        will be in the centre and all elements will either before or after it.
        Elements before the pivot are greater, elements after it are smaller.
        """
        # Set pivot as last element (for convenience)
        pivot_value = ARRAY[end]
        pivot_index = start

        for i in range(start, end):
            STATES[i] = Colors.BLUE
        STATES[end] = Colors.GREEN
        self.game.update_screen()

        # Go through start-end elements and swap with pivot_index
        # whenever value is less than pivots value
        # after swap, increment the pivot_index
        for i in range(start, end):
            # Highlight pivot index and `i` and update screen
            STATES[i] = Colors.YELLOW
            STATES[pivot_index] = Colors.RED
            if i == pivot_index:
                STATES[i] = Colors.ORANGE
            self.game.update_screen()

            if ARRAY[i] < pivot_value:
                ARRAY[i], ARRAY[pivot_index] = ARRAY[pivot_index], ARRAY[i]
                pivot_index += 1
                # Reset old pivot index to blue
                STATES[pivot_index - 1] = Colors.BLUE

            # Reset `i` to blue and update screen
            STATES[i] = Colors.BLUE
            self.game.update_screen()

        # Preform last swap to get the pivot in the middle
        ARRAY[end], ARRAY[pivot_index] = ARRAY[pivot_index], ARRAY[end]
        STATES[end], STATES[pivot_index] = STATES[pivot_index], STATES[end]
        self.game.update_screen()

        for i in range(start, end + 1):
            STATES[i] = Colors.WHITE
        self.game.update_screen()

        return pivot_index

    def sort(self, start: int, end: int) -> None:
        """
        Keep re-partitioning increasingly smaller chunks of the list
        until the list is fully repartitioned, in which case it is sorted.
        """
        # Stop when start reaches end (that section is now sorted)
        if start >= end:
            return

        # get pivot index (middle value, to which things are sorted)
        index = self.partition(start, end)
        # Sort values in the 2 remaining sections (before and after pivot middle value)
        self.sort(start, index - 1)
        self.sort(index + 1, end)


class Game:
    # How far are individual lines from each other
    SEPARATION = 8
    # How fast should the tick rate be
    TICK_RATE = 5
    # Set window parameters
    SIZE = WIDTH, HEIGHT = 400, 350

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SIZE)
        self.fps_clock = pygame.time.Clock()

    def handle_user_quit(self) -> None:
        """If user quits, exit the game and stop program."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def redraw_screen(self) -> None:
        """
        Redraw all lines on the screen.

        This does not update the screen, it only redraws it.
        """
        # Reset screen to black
        self.screen.fill(Colors.BLACK)

        # Map values from array onto pygame window height
        arr = list_remap(ARRAY, (0, Game.HEIGHT))

        # Draw individual lines
        for index, value in enumerate(arr):
            # Round the value before working with it
            # This is necessary because pygame doesn't accept floats
            value = round(value)

            # Start with 10 units gap, draw lines with given separation between them
            x_pos = 10 + index * Game.SEPARATION
            # Subtract the value from height, pygame is inverted on Y axis
            y_pos = Game.HEIGHT - value

            pos1 = (x_pos, Game.HEIGHT)
            pos2 = (x_pos, y_pos)

            color = STATES[index]

            pygame.draw.line(self.screen, color, pos1, pos2)

    def update_screen(self, tick: bool = True) -> None:
        """
        Update the screen accordingly to `redraw_screen`
        also check for user quit and tick (until specified otherwise).
        """
        self.handle_user_quit()
        self.redraw_screen()

        # Update the display and tick when needed
        pygame.display.update()
        if tick:
            self.fps_clock.tick(Game.TICK_RATE)


game = Game()
quick_sort = QuickSort(game)

# Starting timeout
time.sleep(2)

quick_sort.sort(0, len(ARRAY) - 1)
game.update_screen()

# Don't stop straight away
time.sleep(3)
