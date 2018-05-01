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

class car:
	
	def _init_(self, identity):
		this.identity = identity
		#Keep track of first and second (and possibly third) choice on path
		this.path = []
		#Keep track of choices in the past and times perhaps
		this.historicalChoices = {}
	
	#Pick path based on some algorithm and the location you're at and historical travel
	#Also, update historical choices in here
	def choosePath(self, currLocation, algo):
		
class path:
	
	def _init(self, name, cost):
		this.name = name
		this.cost = cost
		
	
		
		
