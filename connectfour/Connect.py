from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from kivy.clock import Clock

import numpy as np
from Mechanics import *

class ConnectFourGrid(GridLayout):
	'''
	This class contains all the objects, methods needed for interfacing the player 
	with the GUI
	'''

	player = True
	with_pc = False
	WinnerYet = False
	pcvspc = False

	spiner = ObjectProperty(None)

	xo_cell_00 = ObjectProperty(None)
	xo_cell_01 = ObjectProperty(None)
	xo_cell_02 = ObjectProperty(None)
	xo_cell_03 = ObjectProperty(None)
	xo_cell_04 = ObjectProperty(None)
	xo_cell_05 = ObjectProperty(None)
	xo_cell_06 = ObjectProperty(None)

   	xo_cell_10 = ObjectProperty(None)
	xo_cell_11 = ObjectProperty(None)
	xo_cell_12 = ObjectProperty(None)
	xo_cell_13 = ObjectProperty(None)
	xo_cell_14 = ObjectProperty(None)
	xo_cell_15 = ObjectProperty(None)
	xo_cell_16 = ObjectProperty(None)

	xo_cell_20 = ObjectProperty(None)
	xo_cell_21 = ObjectProperty(None)
	xo_cell_22 = ObjectProperty(None)
	xo_cell_23 = ObjectProperty(None)
	xo_cell_24 = ObjectProperty(None)
	xo_cell_25 = ObjectProperty(None)
	xo_cell_26 = ObjectProperty(None)

	xo_cell_30 = ObjectProperty(None)
	xo_cell_31 = ObjectProperty(None)
	xo_cell_32 = ObjectProperty(None)
	xo_cell_33 = ObjectProperty(None)
	xo_cell_34 = ObjectProperty(None)
	xo_cell_35 = ObjectProperty(None)
	xo_cell_36 = ObjectProperty(None)

	xo_cell_40 = ObjectProperty(None)
	xo_cell_41 = ObjectProperty(None)
	xo_cell_42 = ObjectProperty(None)
	xo_cell_43 = ObjectProperty(None)
	xo_cell_44 = ObjectProperty(None)
	xo_cell_45 = ObjectProperty(None)
	xo_cell_46 = ObjectProperty(None)

	xo_cell_50 = ObjectProperty(None)
	xo_cell_51 = ObjectProperty(None)
	xo_cell_52 = ObjectProperty(None)
	xo_cell_53 = ObjectProperty(None)
	xo_cell_54 = ObjectProperty(None)
	xo_cell_55 = ObjectProperty(None)
	xo_cell_56 = ObjectProperty(None)

	grid = np.zeros((6,7), dtype=int)

	def __init__(self, *args, **kwargs):
		'''initialises the grid with 6x7 cells, a spinner, and buttons
		'''
		super(ConnectFourGrid, self).__init__(*args, **kwargs)

		self.cells = {
			00:self.xo_cell_00,
			01:self.xo_cell_01,
        	02:self.xo_cell_02,
        	03:self.xo_cell_03,
        	04:self.xo_cell_04,
        	05:self.xo_cell_05,
        	06:self.xo_cell_06,
        	10:self.xo_cell_10,
        	11:self.xo_cell_11,
        	12:self.xo_cell_12,
        	13:self.xo_cell_13,
        	14:self.xo_cell_14,
        	15:self.xo_cell_15,
        	16:self.xo_cell_16,
        	20:self.xo_cell_20,
        	21:self.xo_cell_21,
        	22:self.xo_cell_22,
        	23:self.xo_cell_23,
        	24:self.xo_cell_24,
        	25:self.xo_cell_25,
        	26:self.xo_cell_26,
        	30:self.xo_cell_30,
        	31:self.xo_cell_31,
        	32:self.xo_cell_32,
        	33:self.xo_cell_33,
        	34:self.xo_cell_34,
        	35:self.xo_cell_35,
        	36:self.xo_cell_36,
        	40:self.xo_cell_40,
        	41:self.xo_cell_41,
        	42:self.xo_cell_42,
        	43:self.xo_cell_43,
        	44:self.xo_cell_44,
        	45:self.xo_cell_45,
        	46:self.xo_cell_46,
        	50:self.xo_cell_50,
        	51:self.xo_cell_51,
        	52:self.xo_cell_52,
        	53:self.xo_cell_53,
        	54:self.xo_cell_54,
        	55:self.xo_cell_55,
        	56:self.xo_cell_56
        }

		self.spiner.bind(text=self.spiner_change)

		self.new_game()

	def on_new_game(self, instance):
		'''helper method for starting a new game
		'''
		self.new_game()

	def new_game(self):
		'''starts a new game and sets attributes to start condition
		'''
		self.grid = np.zeros((6,7), dtype=int)
		for key, btn in self.cells.items():
			btn.background_normal = 'images/blank.png'

		self.player_1, self.player_2 = 1, 2
		self.cur_player = self.player_1
		self.WinnerYet = False

		if self.pcvspc:
			self.startpcvspc()

	def spiner_change(self, instance, text):
		'''controls the spinner
		'''
		if text == 'Player vs Player':
			self.with_pc = False
			self.pcvspc = False
			self.new_game()
		if text == 'Player vs PC':
			self.with_pc = True
			self.pcvspc = False
			self.new_game()
		if text == 'PC vs PC':
			self.pcvspc = True
			self.new_game()


	def startpcvspc(self):
		'''lets play 2 pcs against each other
		'''
		noWinnerYet = True
		while noWinnerYet:
			cell_num = move_at_random(self.grid)

			if move_still_possible(self.grid):
				noWinnerYet = False
				self.result_popup()
				return
			
			#last number is column
			col_num  = cell_num%10


			#if move allowed -> do stuff
			if  move_is_correct(self.grid, col_num):
				self.set_symbol(cell_num, col_num, self.cur_player)

			if move_was_winning_move(self.grid, self.cur_player):
				noWinnerYet = False

	def click(self, cell_num):
		'''
		@param cell_num: number of button which is pressed

		by clicking a button on the gui a cell_num(0-56) is passed 
		'''
		#last number is column
		col_num  = cell_num%10
		#if move allowed -> do stuff
		if  move_is_correct(self.grid, col_num):
			self.set_symbol(cell_num, col_num, self.cur_player)
			
			if self.with_pc and not self.WinnerYet:			

				while True: 
					cell_num = move_at_random(self.grid)
					col_num  = cell_num%10

					if move_is_correct(self.grid, col_num):
						self.set_symbol(cell_num, col_num, self.cur_player)
						break

		#no move possible -> end game
		if move_still_possible(self.grid):
			self.result_popup()
			return
	
	def set_symbol(self, cell, num, symbol):
		'''
		@param cell : which button is pressed
		@param num : which column is pressed
		@param symbol: is symbol of current player

		sets state in the grid and moves forward with the game
		'''
		self.grid , x, y = move(self.grid, self.cur_player, num)

		cell = x*10+y
		self.cells[cell].background_normal = 'images/%s.png' % symbol

		if move_was_winning_move(self.grid, self.cur_player):
			self.WinnerYet = True
			self.result_popup()
			return

		if self.cur_player == self.player_1:
			self.cur_player = self.player_2
		else:
			self.cur_player = self.player_1

	def result_popup(self):
		'''pop up for congratulating the user
		'''

		if move_was_winning_move(self.grid, self.cur_player):
			title = 'Congratulation!!!'
			
			if self.cur_player == 1:
				message = '%s wins' %'Blue'
			else:
				message = '%s wins' %'Red'

		elif move_still_possible(self.grid):
			title = 'Draw'
			message = 'Draw'

		new_game_btn = Button(text='Restart', size_hint_y=None, height=50)
		close_btn = Button(text='Close', size_hint_y=None, height=50)
		content = BoxLayout(orientation='vertical')
		content.add_widget(Label(text=message))
		buttons = BoxLayout(orientation='horizontal')

		buttons.add_widget(new_game_btn)
		buttons.add_widget(close_btn)
		content.add_widget(buttons)
		popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(300, 200)
        )
		close_btn.bind(on_release=popup.dismiss)
		new_game_btn.bind(on_press=self.on_new_game)
		new_game_btn.bind(on_release=popup.dismiss)
		popup.open()

	def exit(self):
		App.get_running_app().stop()