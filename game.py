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
        self.mark_active_boats([1100, 30])
        self.mark_active_boats([1100, 200], 'human')
        self._game_logic.setup_game()
        while self._running:
            for event in pygame.event.get():
                # Populate ai boat dictionary
                self._event_handler(event)
            pygame.display.update()

    def _event_handler(self, event):
        """Manages game events"""
        if event.type == pygame.QUIT:
            self._running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._game_status == 'SETUP':
                self._setup_button('Rotate')
                self._listen_for_clicks(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif self._game_status == 'START':
                self._create_sea_map()
                self._vertical_horizontal_lines()
                self._game_status = 'PLAY'
                pygame.draw.rect(self._screen, (0, 0, 0), pygame.Rect(1100, 550, 100, 50))
                pygame.display.update()
            elif self._game_status == 'PLAY':
                self.mark_active_boats([1100, 30])
                self.mark_active_boats([1100, 200], 'human')
                self._setup_button(str(self._game_logic.get_opponent()), 100, 50, (0, 0, 0))
                self._listen_for_clicks(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                self._check_for_winner()
            elif self._game_status == 'END':
                self._check_for_winner()

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

    def _setup_button(self, message, x_size=100, y_size=50, color=(235, 94, 52)):
        """Adding the rotation button on the board"""
        pygame.draw.rect(self._screen, color, pygame.Rect(1100, 550, x_size, y_size))
        text = self._add_text_on_screen(message, 25)
        self._screen.blit(text, (1110, 560))
        pygame.display.update()

    def _add_text_on_screen(self, text, font_size, color=(255, 255, 255)):
        """Takes as a parameter a text and returns the text ready to attach on screen"""
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text = font.render(text, True, color)
        return text

    def mark_active_boats(self, start_pos, player='ai'):
        """It marks active or inactive an enemy vessel if it gets destroyed"""
        vessels = self._game_logic.get_vessels_location()[player]
        boats_list = self._add_text_on_screen(player+' Boats', 20, (235, 0, 0))
        self._screen.blit(boats_list, (start_pos[0], start_pos[1]))
        coord_x_y = [start_pos[0], start_pos[1]+30]
        for vessel in vessels:
            text = self._add_text_on_screen(vessel, 15)
            if vessels[vessel] == ['destroyed']:
                pygame.draw.rect(self._screen, (0, 0, 0), pygame.Rect(coord_x_y[0]+60, coord_x_y[1], 100, 20))
                boat_status = self._add_text_on_screen('Destroyed', 15, (235, 0, 0))
            else:
                boat_status = self._add_text_on_screen('Active', 15, (15, 184, 68))
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

    def _draw_color_box(self, x, y, color, boat_size=1):
        """It draws a color box to represent a ship or shot on the map. Takes the color and coordinates as parameter"""
        if boat_size != 1 and self._game_logic.get_direction() == 'horizontal':
            pygame.draw.rect(self._screen, color, pygame.Rect(x, y, 50*boat_size, 50))
        elif boat_size != 1 and self._game_logic.get_direction() != 'horizontal':
            pygame.draw.rect(self._screen, color, pygame.Rect(x, y, 50, 50*boat_size))
        else:
            pygame.draw.rect(self._screen, color, pygame.Rect(x, y, 50, 50))

    def _draw_ship_on_map(self, coordx, coordy, ship_type, ship_size):
        """
        It draws the ship on the map. Takes coordinates x, y, ship type and ship size
        """
        # Convert coordinates to specific box
        pos = self._convert_click_to_box(coordx, coordy)
        if self._game_logic.get_direction() == 'horizontal' and 50<=pos[0]+(ship_size * 50)<=1050 and 50<=pos[1]<=650:
            # Add coordinates in dictionary for players
            self._game_logic._populate_vessel_dictionary(pos[0], pos[1], ship_type, 'human')
            # Add box on the map
            self._draw_color_box(pos[0], pos[1], (109, 117, 112), ship_size)
        elif self._game_logic.get_direction() == 'vertical' and 50<=pos[0]<=1050 and 50<=pos[1]+(ship_size*50)<=650:
            # Add coordinates in dictionary for players
            self._game_logic._populate_vessel_dictionary(pos[0], pos[1], ship_type, 'human')
            # Add box on the map
            self._draw_color_box(pos[0], pos[1], (109, 117, 112), ship_size)

    def _add_ships_on_map(self, coordx, coordy):
        """This method puts each boat on the map and populates the players dictionary for human"""
        boat_size = {'vessel': 5, 'frigate': 4, 'galleon': 3, 'brig': 2}
        if self._game_logic.get_vessels_location()['human']['vessel'] == []:
            self._draw_ship_on_map(coordx, coordy, 'vessel', 5)
        elif self._game_logic.get_vessels_location()['human']['frigate'] == []:
            self._draw_ship_on_map(coordx, coordy, 'frigate', 4)
        elif self._game_logic.get_vessels_location()['human']['galleon'] == []:
            self._draw_ship_on_map(coordx, coordy, 'galleon', 3)
        else:
            self._draw_ship_on_map(coordx, coordy, 'brig', 2)
            self._game_status = 'START'

    def _listen_for_clicks(self, coordx, coordy):
        """
        It takes two parameters coordinates x and y and activates the proper function
        """
        if 50 < coordx < 1050 and 50 < coordy < 650 and self._game_status == 'SETUP':
            self._add_ships_on_map(coordx, coordy)
        elif 1100 < coordx < 1200 and 550 < coordy < 600 and self._game_status == 'SETUP':
            self._game_logic.set_direction()
        elif 50 < coordx < 1050 and 50 < coordy < 650 and self._game_status == 'PLAY':
            self._load_shots_on_map()   # Load previous shots for current player
            # It doesn't capture players in the right order!!!
            self._draw_shots_on_map(coordx, coordy)     # Player automatically changes
            self._load_shots_on_map('opponent')   # Reload map for the same player to show new shot
            self._load_shots_on_map()   # Load next players shots so he can make a new

    def _draw_shots_on_map(self, coordx, coordy):
        """
        It marks hit or miss shots on enemy map. It checks if shot has already been fired.
        """
        result = self._game_logic.get_cannon_coordinates(coordx, coordy)
        boxes = self._convert_click_to_box(result[1], result[2])
        shots = self._game_logic.get_shots_fired()['human']
        shot_fired = False
        for shot in shots:
            if shots[shot][0] == (boxes[0], boxes[1]):
                shot_fired = True
        if not shot_fired:
            if result[0]:
                self._draw_color_box(boxes[0], boxes[1], (255, 0, 0))
            else:
                self._draw_color_box(boxes[0], boxes[1], (182, 191, 207))

    def _show_game_icon(self, message):
        """
        Shows a message in the middle of the screen
        """
        pygame.display.set_caption(message)
        font = pygame.font.Font(pygame.font.get_default_font(), 35)
        text = font.render(message, True, (255, 255, 255), (255, 0, 0))
        self._screen.blit(text, (450, 700))

    def _load_shots_on_map(self, player='current'):
        """
        Loads all shots fired from current player on the map
        """
        if player == 'current':
            shots_dict = self._game_logic.get_shots_fired()[self._game_logic.get_current_player()]
        else:
            shots_dict = self._game_logic.get_shots_fired()[self._game_logic.get_opponent()]
        self._create_sea_map()
        self._vertical_horizontal_lines()
        for key in shots_dict:
            box_x = shots_dict[key][0][0]
            box_y = shots_dict[key][0][1]
            self._draw_color_box(box_x, box_y, shots_dict[key][1])

    def _check_for_winner(self):
        """
        If some already won, no more clicks available and winner is displayed
        """
        winner = self._game_logic.get_winner()
        if winner[0]:
            self._game_status = 'END'
            winner = self._add_text_on_screen(winner[1]+' WON!', 50, (102, 204, 0))
            self._screen.blit(winner, (400, 300))
