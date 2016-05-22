Connect Four
=========

This is a joint project of Eva, Kanil, Pascal, Anna Lena and Nico for the Game AI course in SS 2016

Connect Four - it's a game! 

written with [Kivy](http://kivy.org "Kivy") (Open source Python library for rapid development of applications)

=========
Task 1.3

The tictactoe.py was modified by changing the size of the grid as well as the way how to check weather a move was a winning move. For this, we combine all the allowed formations of the grid(grid itself, rotated grid, all diagonals with at least 4 cells) and string find() with the current player vector(" 1 1 1 1" or "2 2 2 2").

The files used for this task:
main.py - This starts the kivyapp.
Mechanics.py - The mechanics for the game like making a random move or checking wether a move was a winning move.
ConnectFour.py - The Visualization for the Buttons, slider, popup windows etc. This calls the mechanics of connect four.
connectfour.kv - Creates the widget tree and binds widget properties

=========
For testing: 

* [install](https://kivy.org/#download) kivy for your OS

* add the dependencies:
	
	For OSX users:

		kivy -m pip install numpy

	for linux/windows install dependencies via pip
	
		pip install numpy


* cd into /connectfour 

* to run on OSX

		kivy main.py

	on linux/windows

		python main.py

=========

To build with buildozer

* install [buildozer](https://github.com/kivy/buildozer) with

		pip install buildozer

* and cd to folder one before connectfour and run
	
		buildozer osx release

some tips for building on OSX: 

* use provided buildozer.spec
* if builddir error: change osx.py in buildozer from builddir to build_dir (pullrequest is merged)
* if venv error try downgrading to python 2.7.9 

=========

##### Resources:
* [TicTacToe for Kivy](https://github.com/kgantsov/tictactoe)
* [Wikipedia: ConnectFour](https://en.wikipedia.org/wiki/Connect_Four)
* [ConnectFourAI](http://roadtolarissa.com/connect-4-ai-how-it-works/)
* Lecture of Prof. Dr. Christian Bauckhage at B-IT Bonn: Game AI course