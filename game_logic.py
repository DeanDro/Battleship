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

    def get_cannon_coordinates(self, coordx, coordy):
        """This method takes as parameters the target player, the player that shot, the x and y coordinates and returns
        a list with true if it hit an enemy boat or false if it was a miss and the x, y coordinates"""
        # Each box in the board is 50x50. By dividing coordx with 50 we will get the box before the one the user
        # clicked on. Multiplying by 50 will give us the starting point x of the box the user clicked. Adding
        # 50 will give us the end point of that box. Similar for y. Also we add the color of the box in the
        # list that goes in the dictionary with shots fired to indicated if it was hit or miss.
        box_x = (coordx // 50) * 50 + 1
        box_y = (coordy // 50) * 50 + 1
        miss = True

        target_player = 'human'
        if self._current_player == 'human':
            target_player = 'ai'

        # Each time the particular player shots. It will be added incrementally in the dictionary
        new_key = len(self._shots_fired[self._current_player]) + 1
        self._number_of_shoots += 1
        # we rotate through the types of ships
        for value in self._vessels_location[target_player]:
            boat_size = len(self._vessels_location[target_player][value])
            for i in range(0, boat_size):
                if self._vessels_location[target_player][value][i] == (box_x, box_y):
                    miss = False
                    self._shots_fired[self._current_player][new_key] = [(box_x, box_y), 'red']
                    self._vessels_location[target_player][value][i] = []

                    # Check if boat destroyed
                    if not self._vessels_location[target_player][value]:
                        self._vessels_location[target_player][value] = ['destroyed']

                    # Check if game ended
                    self._winner()
                    self._update_player()
                    # return [True, box_x, box_y]
        if miss:
            self._shots_fired[self._current_player][new_key] = [(box_x, box_y), 'white']
            self._update_player()
            return [False, box_x, box_y]
        else:
            return [True, box_x, box_y]

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
            end_point = x_coord + vessel_size[ship_type] * 50 + (x_point // 50)
            for i in range(x_coord, end_point, 50):
                self._vessels_location[players_turn][ship_type].append((i, y_coord))
        else:
            end_point = y_coord + vessel_size[ship_type] * 50 + (y_point // 50)
            for i in range(y_coord, end_point, 50):
                self._vessels_location[players_turn][ship_type].append((x_coord, i))

    def _winner(self):
        """Checks if someone won the game. Returns a tuple with boolean and winner's name"""
        end_of_game = True
        for player in self._vessels_location:
            winner = player
            for ship_type in self._vessels_location[player]:
                if self._vessels_location[player][ship_type] != ['destroyed']:
                    end_of_game = False
            if end_of_game:
                return end_of_game, winner
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

    def setup_game(self):
        """Starts necessary private methods"""
        self._ai_battle_ships()
