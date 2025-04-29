DISCLAIMER: I probably screwed something up

Project Structure:
.
├── main.py                     # Main application entry point
├── main_menu.py               # GUI for the main menu
├── rewards_from_keys.py       # (Placeholder) GUI and logic for calculating rewards from keys
├── keys_needed_for_pearls.py  # GUI and simulation for calculating required keys
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

Requirements:
- Python 3.7+
- tkinter
- matplotlib
- seaborn
- numpy

Installation:
- git clone https://github.com/SgtSlayer3/Emporium-of-Enigma-Simulator.git
  cd Emporium-of-Enigma-Simulator
- python3 -m venv venv (otional)
  source venv/bin/activate (otional)
- pip install -r requirements.txt

How to run:
- python main.py

Features:
- Main menu allowing the selection of either Rewards from Keys or Keys Needed for pearls
- Keys Needed for pearls
   - Simulates how many Keys are needed to reach a pear goal selected by the users.
   - Results in a Histogram displaying the output across simulations.
- Rewards from Keys
   - Simulates the amount of pearls you will receive from an amount of keys imputed by the user.
   - Results in a Histogram displaying the output across simulations.

Future updates:
- Calculate all rewards from keys.
- Allow the user to togle packs to get an amount of keys instead of just typing in an integer.

Author: sgt slayer
Feel free to message me on discord at **sgt_slayer3** if you have any questions or find any error
