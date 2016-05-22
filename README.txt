Group: Eva Gerlitz, Anna-Lena Popkes, Pascal Wenker, Kanil Patel, Nico Lutz

Task 1.3: Connect four

The visualization of our connect four is done with Kivy, an open source Python library for rapid development of applications (https://kivy.org/#home)

The tictactoe.py was modified by changing the size of the grid as well as the way how to check weather a move was a winning move. For this, we combine all the allowed formations of the grid(grid itself, rotated grid, all diagonals with at least 4 cells) and string_find with the current player vector(" 1 1 1 1" or "2 2 2 2").

The files used for this task:
main.py - This starts the kivyapp.
Mechanics.py - The mechanics for the game like making a random move or checking wether a move was a winning move.
Connect.py - The Visualization for the Buttons, slider, popup windows etc. This calls the mechanics of connect four.
connect.kv - Creates the widget tree and binds widget properties

INSTALLATION:

1) To install Kivy on your OS, please follow the instructions here: https://kivy.org/#download

2) FOR OSX USERES ONLY! 
Add the dependencies via the following command:

kivy -m pip install numpy

3) To run the program from the terminal use the following command:

For OSX:
kivy main.py

For Linux/Windows: 
python main.py