import tkinter as tk
from tkinter import ttk

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # Initialize the parent class
        self.controller = controller  # Store the controller for navigation
        self.create_widgets()  # Create the widgets for the main menu

    def create_widgets(self):
        # Title label
        title = ttk.Label(self, text="Main Menu", font=("Helvetica", 16, "bold"))
        title.grid(row=0, column=0, pady=(20, 5), columnspan=1, sticky="nsew")

        # Navigation buttons
        rewards_button = ttk.Button(self, text="Rewards from Keys", command=lambda: self.controller.show_frame("RewardsFromKeys"))
        rewards_button.grid(row=1, column=0, pady=10, ipadx=10, ipady=5, sticky="nsew")

        keys_button = ttk.Button(self, text="Keys Needed for Pearls", command=lambda: self.controller.show_frame("KeysNeededForPearls"))
        keys_button.grid(row=2, column=0, pady=10, ipadx=10, ipady=5, sticky="nsew")

        # Exit button
        exit_btn = ttk.Button(self, text="Exit", command=self.quit)
        exit_btn.grid(row=3, column=0, pady=20, ipadx=10, ipady=5, sticky="nsew")

        # Configure column expansion
        self.grid_columnconfigure(0, weight=1)