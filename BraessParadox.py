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
import math

class car:
	
	def __init__(self, identity):
		self.identity = identity
		#Keep track of first and second (and possibly third) choice on path
		self.first = ' '
		self.second = ' '
		self.third = ' '
		#Keep track of choices in the past and times perhaps
		#three of three slots in historical choices:
		#each index is a list with [<"Path as a string (for printing purposes perhaps">, avg cost, # times pursued]
		self.historicalChoices = []
		self.northPathData = []
		self.northPathData.append('North')
		self.northPathData.append(0.0)#running avg
		self.northPathData.append(0.0)#number times tried
		self.southPathData = []
		self.southPathData.append('South')
		self.southPathData.append(0.0)
		self.southPathData.append(0.0)
		self.northPathData_Bridge = []
		self.northPathData_Bridge.append('NorthBridge')
		self.northPathData_Bridge.append(0.0)
		self.northPathData_Bridge.append(0.0)
		self.historicalChoices.append(self.northPathData)
		self.historicalChoices.append(self.southPathData)
		self.historicalChoices.append(self.northPathData_Bridge)
		
		
		#Booleans to keep track of last move
		self.justWentNorth = False
		self.justWentNorth_Bridge = False
		self.justWentSouth = False
	
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
	
	

#Save paths and associated costs to the car's historicalChoices list
#Let's say epsilon is 0.1?
#let historical choices be a list of list. First index in the list is a list of the path, the avg return and the number of times tried
#second index is the same for the south path
def eGreedyNoBridge(numberOfCars, epsilon):
	
	cars = createCars(numberOfCars, 'S')
	avgCost = 0.0 #used for the end
	
	#use these as dictionary keys perhaps
	northPath = 'North'
	southPath = 'South'
	
	#Case of no highway, fictitious play
	#Assume other players chose randomly, so should you!!
	timeSum = 0.0
	for i in range(100):
		carsNorth = 0
		carsSouth = 0
		for car in cars:
			#If previous history is north is best ...
			if car.historicalChoices[0][1] <= car.historicalChoices[1][1]:
				bestHistoryPath = 'North'
			else:
				bestHistoryPath = 'South'
			#Assuming epsilon is 0.1 I guess 
			if random.uniform(0, 1) > epsilon:
				#Then follow path that's served best historically
				if bestHistoryPath is northPath:
					car.second = 'A'
					carsNorth += 1
					car.justWentNorth = True
				else:
					car.second = 'B'
					carsSouth += 1
					car.justWentSouth = True
			#Epsilon case		
			else:
				if bestHistoryPath is northPath:
					car.second = 'B'
					carsSouth += 1
					car.justWentSouth = True
				else:
					car.second = 'A'
					carsNorth += 1
					car.justWentNorth = True
		#update all cars costs			
		for car in cars:
			#update historical returns with this new value incorporated into avg
			if car.justWentNorth:
				newAmountOfTimesTried = car.historicalChoices[0][2] + 1
				#multiply avg by number of times tried to get the sum, add the new value and divide by historical times tried + 1
				newAvg = float(car.historicalChoices[0][1] * car.historicalChoices[0][2] + (float(carsNorth/100.0) + 45.0)) / newAmountOfTimesTried
				
				#Update avg and times tried
				car.historicalChoices[0][1] = newAvg
				car.historicalChoices[0][2] = newAmountOfTimesTried
				
				#update boolean for next round
				car.justWentNorth = False
				
				#Update avg cost
				avgCost += float(carsNorth/100.0) + 45.0
				
			else:
				newAmountOfTimesTried = car.historicalChoices[1][2] + 1
				#multiply avg by number of times tried to get the sum, add the new value and divide by historical times tried + 1
				newAvg = float(car.historicalChoices[1][1] * car.historicalChoices[1][2] + (float(carsSouth/100.0) + 45.0)) / newAmountOfTimesTried
				
				#Update avg and times tried
				car.historicalChoices[1][1] = newAvg
				car.historicalChoices[1][2] = newAmountOfTimesTried
				
				#update boolean for next round
				car.justWentSouth = False
				
				#update avg cost
				avgCost += float(carsSouth/100.0) + 45.0
				
		
		avgCost = float(avgCost) / numberOfCars	
		timeSum += avgCost
		avgCost = 0.0
	return(timeSum/100.0)
	
	
	
	
def eGreedy_W_Bridge(numberOfCars, epsilon):
	
	cars = createCars(numberOfCars, 'S')
	avgCost = 0.0 #used for the end
	
	#use these as dictionary keys perhaps
	northPath = 'North'
	southPath = 'South'
	northPathBridge = 'NorthBridge'
	
	#Case of no highway, fictitious play
	#Assume other players chose randomly, so should you!!
	timeSum = 0.0
	for i in range(1000):
		carsNorth = 0
		carsSouth = 0
		carsBridge = 0
		for car in cars:
			#If previous history is north is best ...
			if car.historicalChoices[0][1] <= car.historicalChoices[1][1] and car.historicalChoices[1][1] <= car.historicalChoices[2][1]:
				bestHistoryPath = 'North'
			elif car.historicalChoices[0][1] <= car.historicalChoices[2][1] and car.historicalChoices[2][1] <= car.historicalChoices[1][1]:
				bestHistoryPath = 'North'
			elif car.historicalChoices[1][1] <= car.historicalChoices[0][1] and car.historicalChoices[0][1] <= car.historicalChoices[2][1]:
				bestHistoryPath = 'South'
			elif car.historicalChoices[1][1] <= car.historicalChoices[2][1] and car.historicalChoices[2][1] <= car.historicalChoices[0][1]:
				bestHistoryPath = 'South'
			else:
				bestHistoryPath = 'NorthBridge'
					
				
			#Assuming epsilon is 0.1 I guess 
			if random.uniform(0, 1) >= epsilon:
				#Then follow path that's served best historically
				if bestHistoryPath is northPath:
					car.second = 'A'
					carsNorth += 1
					car.justWentNorth = True
				elif bestHistoryPath is southPath:
					car.second = 'B'
					carsSouth += 1
					car.justWentSouth = True
				else:
					car.second = 'A'
					car.third = 'B'
					carsBridge += 1
					car.justWentNorth_Bridge = True
			#Epsilon case		
			else:
				#Flip coin to pick which of the worst 2 paths to choose
				if bestHistoryPath is northPath:
					goNorthBridge = random.randint(0, 1)
					if goNorthBridge:
						car.second = 'A'
						car.third = 'B'
						carsBridge += 1
						car.justWentNorth_Bridge = True
					else:
						#Go south path
						car.second = 'B'
						carsSouth += 1
						car.justWentSouth = True
				elif bestHistoryPath is southPath:
					goNorthBridge = random.randint(0, 1)
					if goNorthBridge:
						car.second = 'A'
						car.third = 'B'
						carsBridge += 1
						car.justWentNorth_Bridge = True
					else:
						#Go north path
						car.second = 'A'
						carsNorth += 1
						car.justWentNorth = True
				#best path is with bridge
				else:
					goNorth = random.randint(0, 1)
					if goNorth:
						car.second = 'A'
						carsNorth += 1
						car.justWentNorth = True
					else:
						#Go south path
						car.second = 'B'
						carsSouth += 1
						car.justWentSouth = True
		#update all cars costs			
		for car in cars:
			#update historical returns with this new value incorporated into avg
			if car.justWentNorth:
				newAmountOfTimesTried = car.historicalChoices[0][2] + 1
				#multiply avg by number of times tried to get the sum, add the new value and divide by historical times tried + 1
				#need to add cars from bridge strategy as well
				newAvg = float(car.historicalChoices[0][1] * car.historicalChoices[0][2] + (float((carsNorth + carsBridge)/100.0) + 45.0)) / newAmountOfTimesTried
				
				#Update avg and times tried
				car.historicalChoices[0][1] = newAvg
				car.historicalChoices[0][2] = newAmountOfTimesTried
				
				#update boolean for next round
				car.justWentNorth = False
				
				#Update avg cost
				avgCost += float((carsNorth + carsBridge)/100.0) + 45.0
				
			elif car.justWentSouth:
				newAmountOfTimesTried = car.historicalChoices[1][2] + 1
				#multiply avg by number of times tried to get the sum, add the new value and divide by historical times tried + 1
				newAvg = float(car.historicalChoices[1][1] * car.historicalChoices[1][2] + (float((carsSouth + carsBridge)/100.0) + 45.0)) / newAmountOfTimesTried
				
				#Update avg and times tried
				car.historicalChoices[1][1] = newAvg
				car.historicalChoices[1][2] = newAmountOfTimesTried
				
				#update boolean for next round
				car.justWentSouth = False
				
				#update avg cost
				avgCost += float((carsSouth + carsBridge)/100.0) + 45.0
			
			else:
				newAmountOfTimesTried = car.historicalChoices[2][2] + 1
				newAvg = float(car.historicalChoices[2][1] * car.historicalChoices[2][2] + (float((carsSouth + carsBridge)/100.0) + float((carsNorth + carsBridge)/100.0))) / newAmountOfTimesTried
				
				#Update avg and times tried
				car.historicalChoices[2][1] = newAvg
				car.historicalChoices[2][2] = newAmountOfTimesTried
				
				#update boolean for next round
				car.justWentNorth_Bridge = False
				
				#update avg cost
				avgCost += float((carsSouth + carsBridge)/100.0) + float((carsNorth + carsBridge)/100.0)
		
		avgCost = float(avgCost) / numberOfCars	
		timeSum += avgCost
		avgCost = 0
	return(timeSum/1000.0)
	
	
def UCB1NoBridge(numberOfCars):
	
	cars = createCars(numberOfCars, 'S')
	avgCost = 0.0 #used for the end
	
	#use these as dictionary keys perhaps
	northPath = 'North'
	southPath = 'South'
	northPathBridge = 'NorthBridge'
	
	#Case of no highway, fictitious play
	#Assume other players chose randomly, so should you!!
	timeSum = 0.0
	for i in range(100):
		carsNorth = 0
		carsSouth = 0
		for car in cars:
			#First make sure every action has been played at least once
			numberActionsPlayed = (car.historicalChoices[0][2] > 0 and car.historicalChoices[1][2] > 0)
			if numberActionsPlayed == 2:
				#Choose action that maximizes according to UCB1 formula
				North_X_j_t = float(car.historicalChoices[0][1]) + math.sqrt(2.0 * math.log10(i) / car.historicalChoices[0][2]) #avg returns for this car + sqrt(2 log(i) / car.historicalChoices[0][2])
				South_X_j_t = float(car.historicalChoices[1][1]) + math.sqrt(2.0 * math.log10(i) / car.historicalChoices[1][2])
				if North_X_j_t <= South_X_j_t:
					#Go north
					bestHistoryPath = 'North'
					car.second = 'A'
					carsNorth += 1
					car.justWentNorth = True
				else:
					#Go south
					bestHistoryPath = 'South'
					car.second = 'B'
					carsSouth += 1
					car.justWentSouth = True
			elif numberActionsPlayed == 1:
				if car.historicalChoices[0][2] > 0:
					bestHistoryPath = 'South'
					car.second = 'B'
					carsSouth += 1
					car.justWentSouth = True
				else:
					bestHistoryPath = 'North'
					car.second = 'A'
					carsNorth += 1
					car.justWentNorth = True
			else:
				#Pick randomly
				goNorth = random.randint(0, 1)
				if goNorth:
					bestHistoryPath = 'North'
					car.second = 'A'
					carsNorth += 1
					car.justWentNorth = True
				else:
					bestHistoryPath = 'South'
					car.second = 'B'
					carsSouth += 1
					car.justWentSouth = True
				
		#update all cars costs			
		for car in cars:
			#update historical returns with this new value incorporated into avg
			if car.justWentNorth:
				newAmountOfTimesTried = car.historicalChoices[0][2] + 1
				#multiply avg by number of times tried to get the sum, add the new value and divide by historical times tried + 1
				newAvg = float(car.historicalChoices[0][1] * car.historicalChoices[0][2] + (float(carsNorth/100.0) + 45.0)) / newAmountOfTimesTried
				
				#Update avg and times tried
				car.historicalChoices[0][1] = newAvg
				car.historicalChoices[0][2] = newAmountOfTimesTried
				
				#update boolean for next round
				car.justWentNorth = False
				
				#Update avg cost
				avgCost += float(carsNorth/100.0) + 45.0
				
			else:
				newAmountOfTimesTried = car.historicalChoices[1][2] + 1
				#multiply avg by number of times tried to get the sum, add the new value and divide by historical times tried + 1
				newAvg = float(car.historicalChoices[1][1] * car.historicalChoices[1][2] + (float(carsSouth/100.0) + 45.0)) / newAmountOfTimesTried
				
				#Update avg and times tried
				car.historicalChoices[1][1] = newAvg
				car.historicalChoices[1][2] = newAmountOfTimesTried
				
				#update boolean for next round
				car.justWentSouth = False
				
				#update avg cost
				avgCost += float(carsSouth/100.0) + 45.0
				
		
		avgCost = float(avgCost) / numberOfCars	
		timeSum += avgCost
		avgCost = 0.0
	return(timeSum/100.0)

#Generate a random number of the 3
#randomPath = random.choice([1, 2, 3]) 

if __name__ == '__main__':
	numCars = 4000
	X = []
	Y = []

	#E-greedy no bridge -- Makes perfect sense, does worse when E is further from 0.5 obviously but only marginally
	#should do better with >> E when a bridge is present
	#NOTE: TO speed it up, either edit iterations below or change number of iterations for averaging in algorithm above
	
	for i in range(10):
		Y.append(UCB1NoBridge(numCars))
		X.append(numCars)
		numCars+=1000
	plt.title("Average time per car for e-greedy (no highway) ")
	plt.plot(X,Y)
	plt.show()
	
	'''
	for i in range(10):
		#Y.append(eGreedyNoBridge(numCars, 0.1))
		#X.append(numCars)
		print(eGreedyNoBridge(numCars, 0.25))
		numCars+=1000
	#plt.title("Average time per car for e-greedy (no highway) ")
	#plt.plot(X,Y)
	#plt.show()
	
	for i in range(10):
		Y.append(eGreedy_W_Bridge(numCars, 0.2))
		X.append(numCars)
		numCars+=1000
	plt.title("Average time per car for e-greedy (with highway) ")
	plt.plot(X,Y)
	plt.show()
	
	
	
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
	'''

#Case of highway, fictitious play
#Assume other players pick logically
	
	
	
