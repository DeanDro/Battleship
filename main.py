# Author: Konstantinos Drosos
# Date: 5/15/2021
# Description: A battleship game


import tkinter as tk
from game import BattleShip


class Application(tk.Frame):

    """This class represents the starting page of the game"""

    def __init__(self, master):
        """Initializes application and gets tk.root as parameter"""
        super().__init__(master)
        self._master = master
        self._username = tk.StringVar()
        self._create_widget()

    def _create_widget(self):
        """Creates an input for username"""
        name_label = tk.Label(self._master, text="Username", font=('Arial', 15), bg="#000000")
        name_label.configure(bg="#5D05C8")
        input_box = tk.Entry(self._master, textvariable=self._username, font=('Arial', 10))
        name_label.pack()
        input_box.pack()

        # Buttons
        game_button = tk.Button(self.master, text='Start Game', font=('Arial', 15), command=self._start_game)
        cancel_button = tk.Button(self.master, text='Cancel', font=('Arial', 15), command=self._cancel_game)
        game_button.pack()
        cancel_button.pack()

    def _start_game(self):
        """It starts the game"""
        user = self._username.get()
        battleship_game = BattleShip(user)

    def _cancel_game(self):
        """Cancels game"""
        self.master.quit()


root = tk.Tk()
root.geometry('400x400')
root.configure(bg="#5D05C8")
battleship = Application(root)
battleship.mainloop()
