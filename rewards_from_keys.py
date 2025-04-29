import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import seaborn as sns

class RewardsFromKeys(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.strategy_var = tk.StringVar(value="All Chests")
        self.create_widgets()

    def create_widgets(self):
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainMenu"))
        back_button.pack(anchor="nw", padx=5, pady=5)

        tk.Label(self, text="Enter amount of keys:").pack(anchor="w", padx=10, pady=5)
        self.keys_entry = tk.Entry(self)
        self.keys_entry.pack(anchor="w", padx=10)

        tk.Label(self, text="Chest Opening Strategy:").pack(anchor="w", padx=10, pady=5)
        strategies = ["All Chests", "Silver and Gold Chests", "Gold Chests"]
        for strat in strategies:
            tk.Radiobutton(self, text=strat, variable=self.strategy_var, value=strat,
                        command=self.toggle_brown_chest_input).pack(anchor="w", padx=20)

        self.brown_frame = tk.Frame(self)
        self.brown_frame.pack(anchor="w", padx=20, pady=5)

        self.brown_widgets = []
        self.brown_widgets.append(tk.Label(self.brown_frame, text="Open all if there are"))
        self.brown_widgets[-1].pack(side="left")

        self.brown_entry = tk.Entry(self.brown_frame, width=4)
        self.brown_widgets.append(self.brown_entry)
        self.brown_entry.pack(side="left", padx=5)

        self.brown_widgets.append(tk.Label(self.brown_frame, text="or fewer brown chests available"))
        self.brown_widgets[-1].pack(side="left")

        tk.Label(self, text="Number of simulations:").pack(anchor="w", padx=10, pady=(20, 5))
        self.simulations_entry = tk.Entry(self)
        self.simulations_entry.pack(anchor="w", padx=10)
        self.simulations_entry.insert(0, "50000")

        simulate_button = tk.Button(self, text="Run Simulation", command=self.run_simulation)
        simulate_button.pack(anchor="w", padx=10, pady=10)

        self.toggle_brown_chest_input()

    def toggle_brown_chest_input(self):
        if self.strategy_var.get() == "All Chests":
            for widget in self.brown_widgets:
                widget.pack_forget()
            self.controller.geometry("400x345")
        else:
            for widget in self.brown_widgets:
                widget.pack(side="left", padx=2)
            self.controller.geometry("400x345")

    def run_simulation(self):
        try:
            total_keys = int(self.keys_entry.get())
            simulations = int(self.simulations_entry.get())
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter valid numbers for keys and simulations.")
            return

        strategy = self.strategy_var.get()
        try:
            brown_entry_text = self.brown_entry.get()
            if strategy != "All Chests" and brown_entry_text.strip() != "":
                try:
                    brown_threshold = int(brown_entry_text)
                except ValueError:
                    tk.messagebox.showerror("Invalid Input", "Please enter a valid number for brown chest threshold.")
                    return
            else:
                brown_threshold = None
        except ValueError:
            brown_threshold = None

        pearls_gained_list = []

        for _ in range(simulations):
            keys_left = total_keys
            pearls = 0
            free_refreshes_left = 18
            chests = [self.random_chest() for _ in range(9)]

            while keys_left >= 60:
                if strategy == "All Chests":
                    chest_to_open = random.choice(chests)
                    pearls += self.get_pearls(chest_to_open)
                    keys_left -= 60
                    chests.remove(chest_to_open)

                    if len(chests) == 0:
                        if free_refreshes_left > 0:
                            free_refreshes_left -= 1
                        else:
                            if keys_left >= 90:
                                keys_left -= 90
                            else:
                                break  
                        chests = [self.random_chest() for _ in range(9)]

                else:
                    brown_count = sum(1 for c in chests if c == "Brown")
                    if brown_threshold is not None and brown_count <= brown_threshold:
                        while len(chests) > 0:
                            if keys_left < 60:
                                break  
                            chest_to_open = random.choice(chests)
                            pearls += self.get_pearls(chest_to_open)
                            chests.remove(chest_to_open)
                            keys_left -= 60
                        chests = [self.random_chest() for _ in range(9)]
                        continue

                    if strategy == "Gold Chests":
                        eligible_indices = [i for i, c in enumerate(chests) if c == "Gold"]  
                    else:
                        eligible_indices = [i for i, c in enumerate(chests) if c in ["Silver", "Gold"]]  
                    if eligible_indices:
                        while eligible_indices and keys_left >= 60:
                            idx = random.choice(eligible_indices)
                            chest_to_open = chests.pop(idx)
                            pearls += self.get_pearls(chest_to_open)
                            keys_left -= 60
                            eligible_indices = [i for i, c in enumerate(chests) if (strategy == "Silver and Gold Chests" and c in ["Silver", "Gold"]) or (strategy == "Gold Chests" and c == "Gold")]
                        
                        if free_refreshes_left > 0:
                            free_refreshes_left -= 1
                            chests = [self.random_chest() for _ in range(9)]
                        else:
                            if keys_left >= 90:
                                keys_left -= 90
                                chests = [self.random_chest() for _ in range(9)]
                            else:
                                break  
                    elif not chests:
                        chests = [self.random_chest() for _ in range(9)]
                    else:
                        if free_refreshes_left > 0:
                            free_refreshes_left -= 1
                            chests = [self.random_chest() for _ in range(9)]
                        else:
                            if keys_left >= 90:
                                keys_left -= 90
                                chests = [self.random_chest() for _ in range(9)]
                            else:
                                break  

            pearls_gained_list.append(pearls)

        self.plot_graph(pearls_gained_list)

    def plot_graph(self, pearls_gained_list):
        window = tk.Toplevel(self)
        window.title("Pearls Gained per Simulation")

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.hist(pearls_gained_list, bins=20, color='skyblue', edgecolor='black', alpha=0.7)

        avg_pearls = sum(pearls_gained_list) / len(pearls_gained_list)
        ax.axvline(avg_pearls, color='red', linestyle='dashed', linewidth=2, label=f'Avg: {avg_pearls:.2f}')

        ax.set_title("Pearls Gained with Given Keys")
        ax.set_xlabel("Pearls Gained")
        ax.set_ylabel("Number of Simulations")
        ax.legend()

        side_text = ax.text(0.67, 0.88, '', transform=ax.transAxes, fontsize=10, va='top', ha='left', 
                            bbox=dict(facecolor='white', edgecolor='black'))

        def on_hover(event):
            if event.inaxes == ax:
                for annotation in ax.texts:
                    if annotation != side_text:  
                        annotation.remove()

                for bar in bars:
                    if bar.contains(event)[0]:
                        height = bar.get_height()
                        bar_range = f'{int(bar.get_x())} - {int(bar.get_x() + bar.get_width())}'
                        cumulative_percentile = (sum([b.get_height() for b in bars if b.get_x() + b.get_width() <= bar.get_x() + bar.get_width()]) / sum([b.get_height() for b in bars])) * 100

                        ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8, color='black')

                        side_text.set_text(f'Range: {bar_range}\nPercentile: {cumulative_percentile:.2f}% < {int(bar.get_x() + bar.get_width())}')
                        fig.canvas.draw_idle()
                        break

        bars = ax.patches  
        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def random_chest(self):
        roll = random.uniform(0, 1)
        if roll < 0.085:
            return "Gold"
        elif roll < 0.325:
            return "Silver"
        else:
            return "Brown"

    def get_pearls(self, chest_type):
        if chest_type == "Gold":
            return 13.4 
        elif chest_type == "Silver":
            return 4.22
        else:
            return 1.752
