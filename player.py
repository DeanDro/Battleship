
class Player:

    """This class represents a player in the game"""

    def __init__(self, name):
        """The class creates a Player for the game. It takes the username for the player."""
        self._username = name

    def get_username(self):
        """Returns the name of the player"""
        return self._username
