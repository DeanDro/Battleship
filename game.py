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
        self._board_font = pygame.font.SysFont('Arial', 15, bold=pygame.font.Font.bold)
        # What stage of the game we are
        self._game_status = 'SETUP'
        # Board setup files
        self._running = True
        # Creates map and board graphics
        self._create_sea_map()
        self._vertical_horizontal_lines()
        self._game_logic = GameLogic(self._username)
        self.mark_active_boats()
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
        if self._game_status == 'SETUP':
            self._setup_button()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._add_ships_on_map(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

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

    def _setup_button(self):
        """Adding the rotation button on the board"""
        pygame.draw.rect(self._screen, (235, 94, 52), pygame.Rect(1100, 550, 100, 50))
        text = self._add_text_on_screen('Rotate', 25)
        self._screen.blit(text, (1110, 560))
        pygame.display.update()

    def _add_text_on_screen(self, text, font_size, color=(255, 255, 255)):
        """Takes as a parameter a text and returns the text ready to attach on screen"""
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text = font.render(text, True, color)
        return text

    def mark_active_boats(self):
        """It marks active or inactive an enemy vessel if it gets destroyed"""
        vessels = self._game_logic.get_vessels_location()
        boats_list = self._add_text_on_screen('Enemy Boats', 20, (235, 0, 0))
        self._screen.blit(boats_list, (1100, 30))
        coord_x_y = [1100, 60]
        for vessel in vessels['ai']:
            text = self._add_text_on_screen(vessel, 15)
            boat_status = self._add_text_on_screen('Active', 15, (15, 184, 68))
            if vessels['ai'][vessel]['x'] == ['destroyed']:
                boat_status = self._add_text_on_screen('Destroyed', 15, (235, 0, 0))
            self._screen.blit(text, (coord_x_y[0], coord_x_y[1]))
            self._screen.blit(boat_status, (coord_x_y[0]+70, coord_x_y[1]))
            coord_x_y[1] += 30

    def _convert_click_to_box(self, coordx, coordy):
        """This is a helper method. Takes coords from click and returns the actual box coordinates on map"""
        if 50 < coordx < 1050 and 50 < coordy < 650:
            x_pos = (coordx//50) * 50
            y_pos = (coordy//50) * 50
            return x_pos, y_pos
        else:
            return None

    def _draw_color_box(self, x, y, color):
        """It draws a color box to represent a ship or shot on the map. Takes the color and coordinates as parameter"""
        pygame.draw.rect(self._screen, color, pygame.Rect(50, 50, x, y))

    def _add_ships_on_map(self, coordx, coordy):
        """This method puts each boat on the map and populates the players dictionary for human"""
        pos = self._convert_click_to_box(coordx, coordy)
        boat_size = {'vessel': 5, 'frigate': 4, 'galleon': 3, 'brig': 2}
        pos_dic = self._game_logic.get_vessels_location()['human']
        for vessel in pos_dic:
            print(pos_dic)
            if pos is not None:
                self._game_logic._populate_vessel_dictionary(pos[0], pos[1], vessel, 'human')
                mult = boat_size[vessel]
                if self._game_logic.get_direction() == 'horizontal':
                    self._draw_color_box(pos[0]*mult, pos[1], (109, 117, 112))
                else:
                    self._draw_color_box(pos[0], pos[1]*mult, (109, 117, 122))
