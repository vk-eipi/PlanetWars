#!/usr/bin/python

import sys
from StringIO import StringIO
import unittest
from planetwars.universe_firstbot import MyUniverse
from planetwars import Game
from planetwars.planet2 import Planet2
data = '''P 11.393469 11.849382 0 101 1
P 12.566447 5.411861 2 5 5
P 10.220492 18.286904 1 99 5
P 20.511299 1.196454 0 16 2
P 2.275640 22.502311 0 16 2
P 20.031947 16.699531 0 59 3
P 2.754991 6.999233 0 59 3
P 20.145147 13.395844 0 28 2
P 2.641792 10.302921 0 28 2
P 11.750654 0.000000 0 40 3
P 11.036285 23.698764 1 16 3
P 21.090081 23.054830 0 84 3
P 1.696858 0.643934 0 84 3
P 0.000000 5.954007 0 5 1
P 22.786939 17.744758 0 5 1
P 8.248291 17.317346 1 25 3
P 14.538648 6.381419 0 8 3
P 21.707655 15.860644 0 36 2
P 1.079284 7.838121 0 36 2
P 22.319142 8.844038 0 38 5
P 0.467797 14.854727 0 38 5
P 17.001458 10.072576 0 22 1
P 5.785480 13.626189 0 22 1
F 1 6 2 14 13 2
F 2 100 1 2 14 3
F 2 50 1 15 13 12
go
'''

class planetFunctions(unittest.TestCase):
	
	def setUp(self):
		datastream = StringIO(data)
		self.u = MyUniverse(Game, planet_class = Planet2)
		for line in datastream:
			line = line.strip()
			self.u.update(line)
	def testmyplanets(self):
		my_planets = sorted(self.u.my_planets, key=lambda p: p.id)
		n_planets = sorted(self.u.nobodies_planets, key=lambda p: p.id)
		print my_planets[2].needed_def()
		print n_planets[15]
		print my_planets[0].distance(n_planets[15])
		print my_planets[0].breakeven(n_planets[15])
		print my_planets[0].first_turn_profit(n_planets[15], 40)
		print my_planets[0].first_turn_profit(n_planets[0], 40)
		print my_planets[0].first_turn_profit(n_planets[3], 40)
		
if __name__ == '__main__':
	unittest.main()
	sys.stdin = StringIO(data)
	import profitbot
