Connect Four
=========
This is a joint project of Eva, Kanil, Pascal, Anna Lena, Tim and Nico for the Game AI course in SS 2016

Connect Four - it's a game! 

written with [Kivy](http://kivy.org "Kivy") (Open source Python library for rapid development of applications)

=========
To test [install](https://kivy.org/#download) kivy and cd into /connectfour , run

	kivy main.py

To build install [buildozer](https://github.com/kivy/buildozer) with

	pip install buildozer

some tips for building:
* use path to connectfour folder without spaces (is os bug)
* cd to folder one before connectfour and run
	buildozer osx release
* if building of osx: change osx.py in buildozer from builddir to build_dir (is bug)
* use provided buildozer.spec
* if venv error try downgrading to python 2.7.9 

=========

##### Resources:
* [TicTacToe for Kivy](https://github.com/kgantsov/tictactoe)
* [Wikipedia: ConnectFour](https://en.wikipedia.org/wiki/Connect_Four)
* [ConnectFourAI](http://roadtolarissa.com/connect-4-ai-how-it-works/)
* Lecture of Prof. Dr. Christian Bauckhage at B-IT Bonn: Game AI course