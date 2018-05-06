##Possible paths based on https://en.wikipedia.org/wiki/File:Braess_paradox_road_example.svg
#Path 1: Start -> A -> End
#Path 2: Start -> A -> B -> End
#Path 3: Start -> B -> End

#Costs: Start -> A cost is T/100
#		Start -> B cost is 45
#		A -> End cost is 45
#		B -> End cost is T/100
#		A -> B cost is 0



##Algorithms:
#1. Fictitious Play: Assume all other players follow a strategy that doesn't change (can be a mixed strat) and pick your best choice https://en.wikipedia.org/wiki/Fictitious_play
#2. Epsilon Greedy: Choose best historical choice 1-Epsilon of the time and the other time pick randomly
#3. UCB1: Play each action 1 time to get a sample mean payoff (x_j) for each action.
#	Then, Let n_j represent the number of times action j was played so far.
#	Let the iteration you're at be represented as t
#   Play the action j maximizing x_j + sqrt( 2 * log ( t / n_j ) )
#   Observe the reward X_{j,t} and update the empirical mean for the chosen action.
# 	https://jeremykun.com/2013/10/28/optimism-in-the-face-of-uncertainty-the-ucb1-algorithm/

import networkx as nx
from random import randint
import random
import matplotlib.pyplot as plt

class car:
	
	def __init__(self, identity):
		self.identity = identity
		#Keep track of first and second (and possibly third) choice on path
		self.first = ' '
		self.second = ' '
		self.third = ' '
		#Keep track of choices in the past and times perhaps
		self.historicalChoices = {}
	
	#Pick path based on some algorithm and the location you're at and historical travel
	#Also, update historical choices in here
	
def createCars(numCars, location):
	cars = []
	for c in range(numCars):
		newCar = car(c)
		newCar.first = location
		cars.append(newCar)
	return cars

def fictPlayNoBridge(numberOfCars):
	
	cars = createCars(numberOfCars, 'S')

	#Case of no highway, fictitious play
	#Assume other players chose randomly, so should you!!
	timeSum = 0.0
	for i in range(10):
		carsNorth = 0
		carsSouth = 0
		for car in cars:
			goNorth = random.randint(0, 1)
			if goNorth:
				car.second = 'A'
				carsNorth += 1
			else:
				car.second = 'B'
				carsSouth += 1

		northCarCost = (float(carsNorth/100.0) + 45.0)*float(carsNorth)*2
		southCarCost = (float(carsSouth/100.0) + 45.0)*float(carsSouth)*2
		avgCost = float(northCarCost + southCarCost)/numberOfCars
		timeSum += avgCost
	return(timeSum/10.0) #average time is 65.0021285 in 10 iterations
	
def fictPlay_W_Bridge(numberOfCars):
	cars = createCars(numberOfCars, 'S')

	timeSum = 0.0
	for i in range(10):
		carsNorth = 0
		carsSouth = 0
		carsBridge = 0
		for car in cars:
			goNorth = random.randint(0, 1)
			if goNorth:
				car.second = 'A'
				# take the highway?
				if random.randint(0, 1):
					car.third = 'B'
					carsBridge += 1
				else:
					carsNorth += 1

			else:
				car.second = 'B'
				carsSouth +=1

		northCarCost = (float(carsNorth/100.0) + 45.0)*(float(carsNorth)*2 + float(carsBridge))
		southCarCost = (float(carsSouth/100.0) + 45.0)*(float(carsSouth)*2 + float(carsBridge))
		avgCost = float(northCarCost + southCarCost)/numberOfCars
		timeSum += avgCost
	return(timeSum/10.0)

if __name__ == '__main__':
	numCars = 4000
	X = []
	Y = []
	for i in range(10):
		Y.append(fictPlayNoBridge(numCars))
		X.append(numCars)
		numCars+=1000
	plt.title("Average time per car (no highway) ")
	plt.plot(X,Y)
	plt.show()

	X = []
	Y = []
	for i in range(10):
		Y.append(fictPlay_W_Bridge(numCars))
		X.append(numCars)
		numCars+=1000
	plt.title("Average time per car (with highway) ")
	plt.plot(X,Y)
	plt.show()

#Case of highway, fictitious play
#Assume other players pick logically
	
	
	
