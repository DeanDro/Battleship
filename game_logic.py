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

    def set_direction(self):
        """Changes direction from vertical to horizontal and vice versa"""
        if self.direction == 'horizontal':
            self.direction = 'vertical'
        else:
            self.direction = 'horizontal'

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
            end_point = x_coord + vessel_size[ship_type] * 50 + (x_point // 50)
            for i in range(x_coord, end_point, 50):
                self._vessels_location[players_turn][ship_type]['x'].append(i)
            self._vessels_location[players_turn][ship_type]['y'] = [y_coord]
        else:
            end_point = y_coord + vessel_size[ship_type] * 50 + (y_point // 50)
            for i in range(y_coord, end_point, 50):
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

    def _fill_coordinates_tracker(self, coord, list_coordinates, ship_size):
        """Adds poxes to the coordinates tracker to avoid overlap"""
        for i in range(0, ship_size):
            point = coord + (50 * i)
            list_coordinates.append(point)

    def _random_placement_ai_ships(self):
        """It puts enemy ships on random places on the map"""
        vessel_size = {'vessel': 5, 'frigate': 4, 'galleon': 3, 'brig': 2}
        # Collect list of boxes filled with other ships to avoid merge
        boxes_filled = []
        for ship in self._vessels_location['ai']:
            x_max_coord = 1050 - vessel_size[ship] * 50
            y_max_coord = 650 - vessel_size[ship] * 50
            orientation = random.randint(1, 2)

            # Original coordinates for x, y
            x_pos = 0
            y_pos = 0

            # if orientation is 1 then orientation is horizontal, for 2 is vertical
            if orientation == 1:
                self.direction = 'horizontal'
                while y_pos == 0 or x_pos == 0 or y_pos in boxes_filled or x_pos in boxes_filled:
                    # Convert coordinates to a box
                    x_pos = (random.randint(50, x_max_coord) // 50) * 50 + 1
                    y_pos = (random.randint(50, 600) // 50) * 50 + 1
                self._populate_vessel_dictionary(x_pos, y_pos, ship, 'ai')

                if x_pos in boxes_filled:
                    print('Already exists dammash')

                # Add boxes in coordinates taken
                for x_coordinates in self._vessels_location['ai'][ship]['x']:
                    self._fill_coordinates_tracker(x_coordinates, boxes_filled, vessel_size[ship])
                for y_coordinates in self._vessels_location['ai'][ship]['y']:
                    self._fill_coordinates_tracker(y_coordinates, boxes_filled, 1)
                    print(boxes_filled)
            else:
                self.direction = 'vertical'
                print(boxes_filled)
                while y_pos == 0 or x_pos == 0 or y_pos in boxes_filled or x_pos in boxes_filled:
                    x_pos = (random.randint(50, 1050) // 50) * 50 + 1
                    y_pos = (random.randint(50, y_max_coord) // 50) * 50 + 1
                self._populate_vessel_dictionary(x_pos, y_pos, ship, 'ai')
                # Add boxes in coordinates taken
                for x_coordinates in self._vessels_location['ai'][ship]['x']:
                    self._fill_coordinates_tracker(x_coordinates, boxes_filled, 1)
                for y_coordinates in self._vessels_location['ai'][ship]['y']:
                    self._fill_coordinates_tracker(y_coordinates, boxes_filled, vessel_size[ship])

        # We set direction to horizontal as starting point for the human player.
        self.direction = 'horizontal'
        print(self._vessels_location['ai'])

    def _possible_coordinates(self):
        """Return a set of all possible coordinates"""
        set_values = set()
        for i in range(50, 1050, 50):
            for j in range(50, 650, 50):
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
                pos = []
                incomplete = True
                while incomplete:
                    x_pos = (random.randint(50, x_max) // 50) * 50 + 1
                    y_pos = (random.randint(50, 600) // 50) * 50 + 1
                    for i in range(0, vessel_size[ship]):
                        pos.append((x_pos + i * 50, y_pos))
                    check_coord = True
                    for j in pos:
                        if j not in available_coord:
                            check_coord = False
                            break
                    if check_coord:
                        for w in pos:
                            available_coord.remove(w)
                            self._vessels_location['ai'][ship]['x'].append(w[0])
                            self._vessels_location['ai'][ship]['y'] = w[1]
                            incomplete = False
                    else:
                        print(len(pos))
        print(self._vessels_location['ai'])


test = GameLogic('Dickhead')
print(test._ai_battle_ships())
