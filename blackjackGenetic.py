from collections import defaultdict
from random import random
from random import randint

class Deck():
	def __init__(self, numDecks):
		self.numDecks = numDecks
		self.cards = ([i for i in range(2, 11)] + ['A', 'J', 'Q', 'K'])*4*numDecks

	def cardCount(self):
		cardCount = defaultdict(int)
		for card in self.cards:
			cardCount[card] += 1
		return cardCount

	def __str__(self):
		return "Card counts: " + str(self.cardCount())

	def getCard(self):
		if len(self.cards) > 0:
			index = randint(1,len(self.cards)-1)
			card = self.cards[index]
			del self.cards[index]
			# print(self.cards)
			return card
		else:
			print('No cards left!')
			

class Player():
	def __init__(self, number=0, startProbs=None, isDealer=False):
		self.cards = []
		self.score = 0
		self.playerNumber = number
		self.isQuit = False
		self.isBust = False
		self.is21 = False
		self.__featureVector = defaultdict(int)
		self.__weights = self.initWeights()

	def __str__(self):
		# dashes = "-"*self.playerNumber
		dashes = ''
		return f"{dashes}Player {self.playerNumber}: {self.cards}, {self.score}"

	def getFeatureVector(self):
		self.__featureVector["score"] = self.score
		for i in self.cards:
			self.__featureVector[f"{i}Count"] += 1
		return self.__featureVector

	def initWeights(self):
		initWeights = {"scores": 0, "2Count": 0, "3Count": 0, "4Count": 0, "5Count": 0, "6Count": 0,\
			"7Count": 0, "8Count": 0, "9Count": 0, "10Count": 0, "ACount": 0, "JCount": 0, "QCount": 0, "KCount": 0}
		unnormalisedWeights = [random() for i in range(len(initWeights))]
		total = sum(unnormalisedWeights)
		normalisedWeights = [float(i)/total for i in unnormalisedWeights]
		
		
		i = 0
		for weight in initWeights:
			initWeights[weight] = normalisedWeights[i]
			i+=1

		return initWeights

	def getWeights(self):
		return self.__weights

	def updateWeights(self, updatedWeights):
		total = 0
		for weight in updatedWeights:
			total += updatedWeights[weight]
		
		for weight in updatedWeights:
			updatedWeights[weight] /= total

		self.weights = updatedWeights

	def dealCards(self, deck):
		self.cards = []
		self.score = 0
		card1 = deck.getCard()
		card2 = deck.getCard()
		self.cards.append(card1)
		self.cards.append(card2)
		self.calcCardScore()
	
	def getPrediction(self):
		dotProd = 0
		featureVector = self.getFeatureVector()
		weights = self.getWeights()
		for weight in weights:
			dotProd += weights[weight]*featureVector[weight]
		# print(f"Prediction: {dotProd}")
		return 1 if dotProd < 0.5 else 0

	def hit(self, deck):
		self.cards.append(deck.getCard())
		self.calcCardScore()

	def quit(self):
		self.isQuit = True

	def calcCardScore(self):
		self.score = 0
		aceCount = 0
		for card in self.cards:
			if card in ['J', 'Q', 'K']:
				self.score += 10
			elif card != 'A':
				self.score += card
			if card == 'A':
				aceCount += 1
		
		for card in self.cards:
			if card == 'A' and self.score + aceCount - 1 <= 10:
				self.score += 11
			elif card == 'A':
				self.score += 1
		
		if self.score == 21: self.is21 = True
		if self.score > 21: 
			self.isBust = True
			self.score = -21


def table(deck, players):
	"""Currently only one player allowed per game."""
	# Deal
	for player in players:
		player.dealCards(deck)
	
	# print(f"bjG {players[0]}")
	
	# Decisions
	while(not all([player.isBust or player.isQuit or player.is21 for player in players])):
		for player in players:
			if player.isBust or player.isQuit or player.is21: continue
			if player.getPrediction():
				player.hit(deck)
			else:
				player.quit()
		# print(f"bjG {players[0]}")

def casino(deckNumber, players):
	deck = Deck(deckNumber)
	for player in players:
		table(deck, [player])

if __name__ == "__main__":
	# How to call this function
	casino(10, [Player(i) for i in range(1)])
