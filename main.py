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
        self._add_background_image('boat_background.png')
        name_label = tk.Label(self._master, text="Username", font=('Arial', 20), fg='#ffffff')
        name_label.configure(bg="#5D05C8")
        input_box = tk.Entry(self._master, textvariable=self._username, font=('Arial', 10))
        name_label.grid(column=0, row=0, pady=20)
        input_box.grid(column=1, row=0, pady=20)

        # Buttons
        game_button = tk.Button(self.master, text='Start Game', font=('Arial', 15), command=self._start_game)
        cancel_button = tk.Button(self.master, text='Cancel', font=('Arial', 15), command=self._cancel_game)
        game_button.grid(column=0, row=1, padx=40, pady=40)
        cancel_button.grid(column=1, row=1, padx=40, pady=40)

    def _add_background_image(self, photo):
        """
        Takes the picture location and loads it as a background
        """
        background_image = tk.PhotoImage(file=photo)
        background_label = tk.Label(self._master, image=background_image, height=400, width=400)
        background_label.place(x=0, y=0)

    def _start_game(self):
        """It starts the game"""
        user = self._username.get()
        battleship_game = BattleShip(user)

    def _cancel_game(self):
        """Cancels game"""
        self.master.quit()


root = tk.Tk()
root.geometry('400x400')
battleship = Application(root)
battleship.mainloop()
