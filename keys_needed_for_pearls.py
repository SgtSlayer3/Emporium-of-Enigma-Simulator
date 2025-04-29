import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import seaborn as sns

class KeysNeededForPearls(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.strategy_var = tk.StringVar(value="All Chests")
        self.create_widgets()

    def create_widgets(self):
        # Back button to return to the main menu
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainMenu"))
        back_button.pack(anchor="nw", padx=5, pady=5)

        # Entry for the amount of pearls
        tk.Label(self, text="Enter amount of pearls:").pack(anchor="w", padx=10, pady=5)
        self.pearls_entry = tk.Entry(self)
        self.pearls_entry.pack(anchor="w", padx=10)

        # Default values for pearls goal and number of simulations
        self.pearls_entry.insert(0, "1500")

        # Chest opening strategy selection
        tk.Label(self, text="Chest Opening Strategy:").pack(anchor="w", padx=10, pady=5)
        strategies = ["All Chests", "Silver and Gold Chests", "Gold Chests"]
        for strat in strategies: 
            tk.Radiobutton(self, text=strat, variable=self.strategy_var, value=strat, 
                           command=self.toggle_brown_chest_input).pack(anchor="w", padx=20)

        #Frame for brown chest input
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
            target_pearls = int(self.pearls_entry.get())
            simulations = int(self.simulations_entry.get())
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter valid numbers for pearls and simulations.")
            return

        strategy = self.strategy_var.get()
        try:
            brown_threshold = int(self.brown_entry.get()) if strategy != "All Chests" else None
        except ValueError:
            brown_threshold = None

        keys_needed_list = []

        #Run the simulation for the specified number of times
        for _ in range(simulations):
            pearls = 0
            keys_used = 0
            free_refreshes_left = 18
            chests = [self.random_chest() for _ in range(9)]

            # Loop until the target pearls are reached
            while pearls < target_pearls:
                # Check if there are any chests left to open
                if strategy == "All Chests":
                    chest_to_open = random.choice(chests)
                    pearls += self.get_pearls(chest_to_open)
                    keys_used += 60
                    chests.remove(chest_to_open)

                    if len(chests) == 0:
                        chests = [self.random_chest() for _ in range(9)]

                else:
                    brown_count = sum(1 for c in chests if c == "Brown")
                    # Check if the brown threshold is reached
                    if brown_threshold is not None and brown_count <= brown_threshold:
                        while len(chests) > 0:
                            if pearls >= target_pearls:
                                break 
                            chest_to_open = random.choice(chests)
                            pearls += self.get_pearls(chest_to_open)
                            keys_used += 60
                            chests.remove(chest_to_open)

                        chests = [self.random_chest() for _ in range(9)]
                        continue
                    # Check if there are any eligible chests to open based on the strategy                                       
                    eligible_indices = [i for i, c in enumerate(chests) if (strategy == "Silver and Gold Chests" and c in ["Silver", "Gold"]) or (strategy == "Gold Chests" and c == "Gold")]
                    if eligible_indices:
                        while eligible_indices and pearls < target_pearls:
                            idx = random.choice(eligible_indices)
                            chest_to_open = chests.pop(idx)
                            pearls += self.get_pearls(chest_to_open)
                            keys_used += 60
                            if pearls >= target_pearls:
                                break
                            eligible_indices = [i for i, c in enumerate(chests) if (strategy == "Silver and Gold Chests" and c in ["Silver", "Gold"]) or (strategy == "Gold Chests" and c == "Gold")]
                        if free_refreshes_left > 0:
                            free_refreshes_left -= 1
                            chests = [self.random_chest() for _ in range(9)]  
                        else:
                            keys_used += 90  
                            chests = [self.random_chest() for _ in range(9)]  
                    else:
                        if free_refreshes_left > 0:
                            free_refreshes_left -= 1
                            chests = [self.random_chest() for _ in range(9)]  
                        else:
                            keys_used += 90  
                            chests = [self.random_chest() for _ in range(9)]  

            keys_needed_list.append(keys_used)

        self.plot_graph(keys_needed_list)

    # Plotting the graph using matplotlib
    def plot_graph(self, pearls_gained_list):
        window = tk.Toplevel(self)
        window.title("Keys needed per Simulation")

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.hist(pearls_gained_list, bins=20, color='skyblue', edgecolor='black', alpha=0.7)

        avg_pearls = sum(pearls_gained_list) / len(pearls_gained_list)
        ax.axvline(avg_pearls, color='red', linestyle='dashed', linewidth=2, label=f'Avg: {avg_pearls:.2f}')

        percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        percentile_values = np.percentile(pearls_gained_list, percentiles)
        for p, value in zip(percentiles, percentile_values):
            ax.axvline(value, color='green', linestyle='dotted', linewidth=1, label=f'{p}%: {value:.0f}')

        ax.set_title("Keys Needed to reach target pearls")
        ax.set_xlabel("Keys")
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
        roll = random.uniform(0, 1)
        if chest_type == "Gold":
            if roll < 0.02:
                return 100
            elif roll < 0.08:
                return 50
            elif roll < 0.50:
                return 20
            else:
                return 0
        elif chest_type == "Silver":
            if roll < 0.005:
                return 100
            elif roll < 0.065:
                return 20
            elif roll < 0.485:
                return 6
            else:
                return 0
        else:  # Brown
            if roll < 0.003:
                return 100
            elif roll < 0.11:
                return 6
            elif roll < 0.515:
                return 2
            else:
                return 0
