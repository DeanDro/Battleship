# In this class we will hold all decisions made for AI in the game as well as respond to user moves

from player import Player


class GameLogic:

    """
    This class manages all decisions made by AI and response to user interaction.
    """

    def __init__(self, human_name):
        """This class will initialize a battleship game. Takes as an argument the username given"""

        # We add some dam data for testing the app
        self._vessels_location = {'human': {'vessel': {'x': [], 'y': []},
                                            'frigate': {'x': [], 'y': []},
                                            'galleon': {'x': [], 'y': []},
                                            'brig': {'x': [], 'y': []}
                                            },
                                  'ai': {'vessel': {'x': [], 'y': []},
                                         'frigate': {'x': [], 'y': []},
                                         'galleon': {'x': [], 'y': []},
                                         'brig': {'x': [], 'y': []}
                                         }
                                  }
        self._shots_fired = {'human': {}, 'ai': {}}
        self._human = Player(human_name)
        self.direction = 'horizontal'
        self._ai = Player('Computer')

    def get_vessels_location(self):
        """Method to return the dictionary with the vessels locations."""
        return self._vessels_location

    def get_shots_fired(self):
        """Method to return the dictionary with the shots fired"""
        return self._shots_fired

    def get_direction(self):
        """It returns the direction for placing the boat"""
        return self.direction

    def get_cannon_coordinates(self, coordx, coordy, target_player, current_player):
        """This method takes as parameters the target player, the player that shot, the x and y coordinates and returns
        true if it hit an enemy boat or false if it was a miss"""
        # Each box in the board is 50x50. By dividing coordx with 50 we will get the box before the one the user
        # clicked on. Multiplying by 50 will give us the starting point x of the box the user clicked. Adding
        # 50 will give us the end point of that box. Similar for y. Also we add the color of the box in the
        # list that goes in the dictionary with shots fired to indicated if it was hit or miss.
        box_x = (coordx // 50) * 50 + 1
        box_y = (coordy // 50) * 50 + 1

        # Check x, y and boat were hit. We store boat type to remove from list if it is destroyed
        hit_x = False
        hit_y = False
        boat = ''

        # Each time the particular player shots. It will be added incrementally in the dictionary
        new_key = len(self._shots_fired[current_player]) + 1
        # we rotate through the types of ships
        for value in self._vessels_location[target_player]:
            boat_blocks_x = len(self._vessels_location[target_player][value]['x'])
            boat_blocks_y = len(self._vessels_location[target_player][value]['y'])
            for i in range(0, boat_blocks_x):
                if self._vessels_location[target_player][value]['x'][i] == box_x:
                    hit_x = True
            for i in range(0, boat_blocks_y):
                if self._vessels_location[target_player][value]['y'][i] == box_y:
                    hit_y = True
                    boat = value
        if hit_y and hit_x:
            self._shots_fired[current_player][new_key] = [box_x, box_x + 49, box_y, box_y + 49, 'red']
            self._vessels_location[target_player][boat]['x'].remove(box_x)
            self._vessels_location[target_player][boat]['y'].remove(box_y)
            # Check if boat destroyed
            if not self._vessels_location[target_player][boat]['x']:
                self._vessels_location[target_player][boat]['x'] = ['destroyed']
                self._vessels_location[target_player][boat]['y'] = ['destroyed']

            # Check if game ended
            self._winner()
            return True
        else:
            self._shots_fired[current_player][new_key] = [box_x, box_x + 49, box_y, box_y + 49, 'white']
            return False

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
            end_point = vessel_size[ship_type] * 50 + (x_point // 50)
            for i in range(x_coord, end_point, 50):
                self._vessels_location[players_turn][ship_type]['x'].append(i)
            self._vessels_location[players_turn][ship_type]['y'] = [y_coord]
        else:
            end_point = vessel_size[ship_type] * 50 + (y_point // 50)
            for i in range(x_coord, end_point, 50):
                self._vessels_location[players_turn][ship_type]['y'].append(i)
            self._vessels_location[players_turn][ship_type]['x'] = [x_coord]

    def _winner(self):
        """Checks if someone won the game. Returns a tuple with boolean and winner's name"""
        end_of_game = True
        for player in self._vessels_location:
            winner = player
            for ship_type in self._vessels_location[player]:
                for ship_coord in self._vessels_location[player][ship_type]:
                    if self._vessels_location[player][ship_type][ship_coord] != ['destroyed']:
                        end_of_game = False
            if end_of_game:
                return end_of_game, winner
        return False, None
