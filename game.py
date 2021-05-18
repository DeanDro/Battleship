"""This class starts the battleship game and works as presentation layer"""
import pygame
import sys
from game_logic import GameLogic


class BattleShip:

    """Represents a battleship game"""

    def __init__(self, username):
        """Initiates the game and takes as a parameter the users name"""
        pygame.init()
        self._screen = pygame.display.set_mode((1380, 800))
        self._username = username
        # What stage of the game we are
        self._game_status = 'SETUP'
        self._running = True
        self._create_sea_map()
        self._vertical_horizontal_lines()
        self._game_logic = GameLogic(self._username)
        while self._running:
            for event in pygame.event.get():
                self._event_handler(event)
            pygame.display.update()

    def _event_handler(self, event):
        """Manages game events"""
        if event.type == pygame.QUIT:
            self._running = False
            pygame.quit()
            sys.exit()

    def _create_sea_map(self):
        """It creates the sea map for the ships"""
        pygame.draw.rect(self._screen, (126, 5, 247), pygame.Rect(50, 50, 1000, 600))
        pygame.display.flip()

    def _vertical_horizontal_lines(self):
        """Draws vertical and horizontal white lines on sea board"""
        for i in range(1, 21):
            pygame.draw.rect(self._screen, (255, 255, 255), pygame.Rect(i*50, 50, 1, 600))
        for j in range(1, 13):
            pygame.draw.rect(self._screen, (255, 255, 255), pygame.Rect(50, j*50, 1000, 1))

    def _boats_setup(self):
        """It puts the human user boats on the map"""
        data = self._game_logic.get_vessels_location()

