# Author: Konstantinos Drosos
# Date: 5/15/2021
# Description: A battleship game


import tkinter as tk
from tkinter import *
from game import BattleShip
import os


class Application(tk.Frame):

    """This class represents the starting page of the game"""

    def __init__(self, master, image):
        """Initializes application and gets tk.root as parameter"""
        super().__init__(master)
        self._master = master
        self._background_image = image
        self._username = tk.StringVar()
        self._create_widget()

    def _create_widget(self):
        """Creates an input for username"""
        name_label = tk.Label(self._master, text="Username", font=('Arial', 20), fg='#ffffff')
        name_label.configure(bg="#524A35")
        input_box = tk.Entry(self._master, textvariable=self._username, font=('Arial', 10))
        name_label.grid(column=0, row=0, pady=20)
        input_box.grid(column=1, row=0, pady=20)

        # Buttons
        game_button = tk.Button(self._master, text='Start Game', font=('Arial', 15), command=self._start_game)
        cancel_button = tk.Button(self._master, text='Cancel', font=('Arial', 15), command=self._cancel_game)
        game_button.grid(column=0, row=1, padx=40, pady=40)
        cancel_button.grid(column=1, row=1, padx=40, pady=40)

    def _start_game(self):
        """It starts the game"""
        user = self._username.get()
        battleship_game = BattleShip(user)

    def _cancel_game(self):
        """Cancels game"""
        self.master.quit()

    def _add_background_image(self):
        """
        Returns a photo image file for the background image
        """
        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(base_folder, self._background_image)
        photo = tk.PhotoImage(file=image_path)

        photo_label = tk.Label(self._master, image=photo)
        photo_label.place(x=0, y=0, relwidth=1, relheight=1)


root = tk.Tk()
root.geometry('400x400')
root.configure(bg='#524A35')
battleship = Application(root, 'boat_background.png')
battleship.mainloop()
