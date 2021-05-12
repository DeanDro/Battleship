# In this class we will hold all decisions made for AI in the game as well as respond to user moves

from player import Player

class GameLogic:

    """
    This class manages all decisions made by AI and response to user interaction.
    """

    def __init__(self, human_name):
        """This class will initialize a battleship game. Takes as an argument the username given"""

        # We add some dam data for testing the app
        self._vessels_location = {'human': {'vessel': {'x': [0, 51, 101, 151, 201],
                                                       'y': [0]}},
                                  'ai': {'vessel': {'x': [51], 'y': [0, 51 ]}}}
        self._shots_fired = {'human': {}, 'ai': {}}
        self._human = Player(human_name)
        self._ai = Player('Computer')

    def get_vessels_location(self):
        """Method to return the dictionary with the vessels locations."""
        return self._vessels_location

    def get_shots_fired(self):
        """Method to return the dictionary with the shots fired"""
        return self._shots_fired

    def get_cannon_coordinates(self, coordx, coordy, target_player, current_player):
        """This method takes as parameters the target player, the player that shot, the x and y coordinates and returns
        true if it hit an enemy boat or false if it was a miss"""
        # Each box in the board is 50x50. By dividing coordx with 50 we will get the box before the one the user
        # clicked on. Multiplying by 50 will give us the starting point x of the box the user clicked. Adding
        # 50 will give us the end point of that box. Similar for y. Also we add the color of the box in the
        # list that goes in the dictionary with shots fired to indicated if it was hit or miss.
        box_x = coordx // 50 + 50
        box_y = coordy // 50 + 49
        # Each time the particular player shots. It will be added incrementally in the dictionary
        new_key = len(self._shots_fired[current_player]) + 1
        # we rotate through the types of ships
        for key, value in self._vessels_location[target_player].items():
            # we rotate through x and y coordinates
            for key_2, value_2 in value.items():
                boat_blocks = len(value_2)
                # we iterate through values in the list for the boat
                for i in range(0, boat_blocks):
                    if value_2[i] == coordx:
                        self._shots_fired[current_player][new_key] = [box_x, box_x + 50, box_y, box_y + 50, 'red']
                        # Here we check if we have sunk the enemy vessel and if we have, we replace the coordinates with
                        # the word destroyed
                        value_2.pop(i)
                        if not value_2:
                            value_2 = 'destroyed'
                return True
            else:
                self._shots_fired[current_player][new_key] = [box_x, box_x + 50, box_y, box_y + 50, 'red']
                return False


test = GameLogic('Dude')
print(test.get_cannon_coordinates(73, 72, 'ai', 'human'))
print(test.get_cannon_coordinates(73, 72, 'ai', 'human'))
ai_shot = test.get_shots_fired()
print(ai_shot['human'])