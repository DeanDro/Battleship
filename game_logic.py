# In this class we will hold all decisions made for AI in the game as well as respond to user moves
import random

from player import Player


class GameLogic:

    """
    This class manages all decisions made by AI and response to user interaction.
    """

    def __init__(self, human_name):
        """This class will initialize a battleship game. Takes as an argument the username given"""

        # We add some dam data for testing the app
        self._vessels_location = {'human': {'vessel': [],
                                            'frigate': [],
                                            'galleon': [],
                                            'brig': []
                                            },
                                  'ai': {'vessel': [],
                                         'frigate': [],
                                         'galleon': [],
                                         'brig': []
                                         }
                                  }
        self._shots_fired = {'human': {}, 'ai': {}}
        self._human = Player(human_name)
        self.direction = 'horizontal'
        self._ai = Player('ai')
        self._number_of_shoots = 0
        self._current_player = 'human'
        # Variable to store the size of each boat
        self._ai_targets = {'vessel': 5, 'frigate': 4, 'galleon': 3, 'brig': 2}
        # Variable to store if there is an active target for ai
        self._active_target = {'active': False, 'coord': None}

    def get_vessels_location(self):
        """Method to return the dictionary with the vessels locations."""
        return self._vessels_location

    def get_shots_fired(self):
        """Method to return the dictionary with the shots fired"""
        return self._shots_fired

    def get_direction(self):
        """It returns the direction for placing the boat"""
        return self.direction

    def set_direction(self):
        """Changes direction from vertical to horizontal and vice versa"""
        if self.direction == 'horizontal':
            self.direction = 'vertical'
        else:
            self.direction = 'horizontal'

    def get_number_shots(self):
        """Returns the number of shots fired"""
        return self._number_of_shoots

    def _update_player(self):
        """Updates players turn"""
        if self._current_player == 'human':
            self._current_player = 'ai'
        else:
            self._current_player = 'human'

    def get_current_player(self):
        """Return players turn"""
        return self._current_player

    def get_opponent(self):
        """Get the opponent player"""
        if self._current_player == 'human':
            return 'ai'
        return 'human'

    def get_winner(self):
        """
        Returns tuple with true and winner's name if there is a winner already otherwise returns False, None
        """
        return self._winner()

    def get_cannon_shots(self, coordx, coordy):
        """
        This method takes as parameters the target player, the player that shot, the x and y coordinates and returns
        a list with true if it hit an enemy boat or false if it was a miss and the x, y coordinates
        """
        # Each box in the board is 50x50. By dividing coordx with 50 we will get the box before the one the user
        # clicked on. Multiplying by 50 will give us the starting point x of the box the user clicked. Adding
        # 50 will give us the end point of that box. Similar for y. Also we add the color of the box in the
        # list that goes in the dictionary with shots fired to indicated if it was hit or miss.

        if not self._winner()[0]:
            box_x = (coordx // 50) * 50 + 1
            box_y = (coordy // 50) * 50 + 1

            # Check if the player has already shot this box
            if (box_x, box_y) not in self._shots_fired[self._current_player]:
                target_player = self.get_opponent()
                for value in self._vessels_location[target_player]:
                    for loc in self._vessels_location[target_player][value]:

                        # Check shot hit vessel
                        if loc == (box_x, box_y):
                            self._shots_fired[self._current_player][(box_x, box_y)] = [(box_x, box_y), (255, 0, 0)]
                            self._update_vessels(box_x, box_y, target_player, value)

                            # Check boat destroyed
                            if self._check_boat_destroyed(target_player, value):
                                self._vessels_location[target_player][value] = ['destroyed']

                            self._update_player()
                            return [True, box_x, box_y]

                # The player didn't hit an enemy boat
                self._shots_fired[self._current_player][(box_x, box_y)] = [(box_x, box_y), (182, 191, 207)]
                self._update_player()
                return [False, box_x, box_y]

            return [False, box_x, box_y]

    def _check_boat_destroyed(self, target_player, vessel):
        """
        Helper method to check if a boat has been destroyed. Takes as parameters target player and vessel and returns
        True if the vessel was destroyed
        """
        destroyed = True
        for coord in self._vessels_location[target_player][vessel]:
            if not coord == ['hit']:
                destroyed = False
        return destroyed

    def _populate_vessel_dictionary(self, x_point, y_point, ship_type, players_turn):
        """
        This method takes from the user where the boats are placed in the map and populates the dictionary with their
        coordinates
        """
        # length for each boat
        vessel_size = {'vessel': 5, 'frigate': 4, 'galleon': 3, 'brig': 2}

        # Adjust x, y coord for boat
        x_coord = (x_point // 50) * 50 + 1
        y_coord = (y_point // 50) * 50 + 1

        if self.direction == 'horizontal':
            end_point = x_coord + vessel_size[ship_type] * 50
            for i in range(x_coord, end_point, 50):
                self._vessels_location[players_turn][ship_type].append((i, y_coord))
        else:
            end_point = y_coord + vessel_size[ship_type] * 50
            for i in range(y_coord, end_point, 50):
                self._vessels_location[players_turn][ship_type].append((x_coord, i))

    def _winner(self):
        """Checks if someone won the game. Returns a tuple with boolean and winner's name"""
        for player in self._vessels_location:
            end_of_game = True
            for ship_type in self._vessels_location[player]:
                if self._vessels_location[player][ship_type] != ['destroyed']:
                    end_of_game = False
            if end_of_game:
                return end_of_game, player
        return False, None

    def _fill_coordinates_tracker(self, coord, list_coordinates, ship_size):
        """Adds poxes to the coordinates tracker to avoid overlap"""
        for i in range(0, ship_size):
            point = coord + (50 * i)
            list_coordinates.append(point)

    def _possible_coordinates(self):
        """Return a set of all possible coordinates"""
        set_values = set()
        # Because we count coordinates from 51 growing by 50, we will start possible options from 51
        for i in range(51, 1050, 50):
            for j in range(51, 650, 50):
                set_values.add((i, j))
        return set_values

    def _ai_battle_ships(self):
        """Populates battle ships for ai in random locations"""
        vessel_size = {'vessel': 5, 'frigate': 4, 'galleon': 3, 'brig': 2}
        available_coord = self._possible_coordinates()
        for ship in self._vessels_location['ai']:
            orientation = random.randint(1, 2)
            if orientation == 1:
                x_max = 1050 - (vessel_size[ship] * 50)
                incomplete = True
                while incomplete:
                    pos = []
                    x_pos = (random.randint(50, x_max) // 50) * 50 + 1
                    y_pos = (random.randint(50, 600) // 50) * 50 + 1
                    for i in range(0, vessel_size[ship]):
                        pos.append((x_pos + i * 50, y_pos))
                    check_coord = True
                    # Check if a ship already in that location
                    for j in pos:
                        if j not in available_coord:
                            check_coord = False
                    if check_coord:
                        self._vessels_location['ai'][ship] = pos
                        incomplete = False
            else:
                y_max = 650 - (vessel_size[ship] * 50)
                incomplete = True
                while incomplete:
                    pos = []
                    x_pos = (random.randint(50, 1000) // 50) * 50 + 1
                    y_pos = (random.randint(50, y_max) // 50) * 50 + 1
                    for i in range(0, vessel_size[ship]):
                        pos.append((x_pos, y_pos + i * 50))
                    check_coord = True
                    for j in pos:
                        if j not in available_coord:
                            check_coord = False
                    if check_coord:
                        self._vessels_location['ai'][ship] = pos
                        incomplete = False

        # For testing print ai positions
        # print(self._vessels_location['ai'])

    def setup_game(self):
        """Starts necessary private methods"""
        self._ai_battle_ships()

    def _coord_converter(self, x, y):
        """Takes coordinates and converts them to specific box coordinates"""
        point_x = (x // 50) * 50 + 1
        point_y = (y // 50) * 50 + 1
        return point_x, point_y

    def _update_active_targets(self, x, y):
        if self._shots_fired['ai'][(x, y)][1] == (255, 0, 0):
            self._active_target = {'active': True, 'coord': (x, y)}

    def get_ai_response(self):
        """
        A method for all the moves that the AI will do in the game
        """
        if self._active_target['active']:
            x = self._active_target['coord'][0]
            y = self._active_target['coord'][1]
            if self._active_target['coord'][0] < 1001 and not self._shots_fired['ai'][(x+50, y)]:
                self.get_cannon_shots(x+50, y)
                self._update_active_targets(x+50, y)
            elif self._active_target['coord'][0] > 100 and not self._shots_fired['ai'][(x-50, y)]:
                self.get_cannon_shots(x-50, y)
                self._update_active_targets(x-50, y)
            elif self._active_target['coord'][1] > 100 and not self._shots_fired['ai'][(x, y-50)]:
                self.get_cannon_shots(x, y-50)
                self._update_active_targets(x, y-50)
            elif self._active_target['coord'][1] < 600 and not self._shots_fired['ai'][(x, y+50)]:
                self.get_cannon_shots(x, y+50)
                self._update_active_targets(x, y+50)
            self._update_player()
        else:
            rand_x = random.randint(50, 1050)
            rand_y = random.randint(50, 650)
            miss = True
            points = self._coord_converter(rand_x, rand_y)
            for boat in self._vessels_location['human']:
                for loc in self._vessels_location['human'][boat]:
                    if loc == (points[0], points[1]):
                        miss = False
                        self._shots_fired['ai'][(points[0], points[1])] = [(points[0], points[1]), (255, 0, 0)]
                        self._active_target = {'active': True, 'coord': (rand_x, rand_y)}
            if miss:
                self._shots_fired['ai'][(points[0], points[1])] = [(points[0], points[1]), (182, 191, 207)]
            self._update_player()

    def _update_vessels(self, coordx, coordy, target_player, ship):
        """
        Takes the coordinates, target player and ship to update vessels dictionary when a vessel is hit. Coordinates
        are in tuples, target_player and ship a string
        """
        for i in range(len(self._vessels_location[target_player][ship])):
            if self._vessels_location[target_player][ship][i] == (coordx, coordy):
                self._vessels_location[target_player][ship][i] = ['hit']
