import tkinter as tk
from tkinter import ttk
from main_menu import MainMenu
from rewards_from_keys import RewardsFromKeys
from keys_needed_for_pearls import KeysNeededForPearls

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Key and Pearl Calculator")
        self.geometry("200x300") 
        self.resizable(False, False)

        self.frames = {}

        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        content_frame = ttk.Frame(container)
        content_frame.pack(fill="both", expand=True)

        for F in (MainMenu, RewardsFromKeys, KeysNeededForPearls):
            page_name = F.__name__
            frame = F(parent=content_frame, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
