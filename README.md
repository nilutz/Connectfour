Connect Four
=========
This is a joint project of Eva, Kanil, Pascal, Anna Lena and Nico for the Game AI course in SS 2016

Connect Four - it's a game! 

written with [Kivy](http://kivy.org "Kivy") (Open source Python library for rapid development of applications)

=========
* To test: [install](https://kivy.org/#download) kivy for your OS

* and add the dependencies

		kivy -m pip install numpy

* cd into /connectfour , run

		kivy main.py

	on linux/windows

		python main.py


To build install [buildozer](https://github.com/kivy/buildozer) with

	pip install buildozer



some tips for building on OSX: 
* cd to folder one before connectfour and run
	buildozer osx release
* use provided buildozer.spec
* if builddir error: change osx.py in buildozer from builddir to build_dir (pullrequest is merged)
* if venv error try downgrading to python 2.7.9 

=========

##### Resources:
* [TicTacToe for Kivy](https://github.com/kgantsov/tictactoe)
* [Wikipedia: ConnectFour](https://en.wikipedia.org/wiki/Connect_Four)
* [ConnectFourAI](http://roadtolarissa.com/connect-4-ai-how-it-works/)
* Lecture of Prof. Dr. Christian Bauckhage at B-IT Bonn: Game AI course