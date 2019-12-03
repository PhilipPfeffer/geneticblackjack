from collections import defaultdict
from random import random
from random import randint
from random import sample
import numpy as np
from blackjackGenetic import Player

class GeneticModel(object):
    def __init__(self):
        self.genNum = 0

    def __str__(self):
        return str([str(player) for player in self.players])

    def initializeGeneration(self, n):
        self.players = [Player(i) for i in range(n)]

    def normalize(self, pdf):
        total = sum(pdf)
        return [float(i)/total for i in pdf]

    def getAvgScore(self):
        avg = 0
        for player in self.players:
            avg += player.score
        avg /= len(self.players)
        return avg

    def train(self, playersPerGen, threshhold):
        self.select(threshhold)
        self.crossover(playersPerGen)
        self.mutate()

    def select(self, threshhold):
        # Returns parents of next generation by removing all:
        #  - bust players
        #  - players who got blackjack (pure luck, no genes)
        #  - players who got above a certain score (threshhold)
        selection = []
        for player in self.players:
            if not player.isBust and player.score >= threshhold and not (len(player.cards)==2 and player.is21):
                selection.append(player)

        self.parents = selection
        # return selection # the parents of the next gen

    def crossover(self, childrenNum):
        self.genNum += 1
        children = []
        numParents = len(self.parents)
        numParents = numParents if numParents % 2 == 0 else numParents - 1
        if numParents < 2: pass #init randomly?
        # print(f"Number of parents: {numParents}")
        # check even & odd
        for i in range(0,numParents,2):
            if i >= childrenNum: break
            parentWeights0 = self.parents[i].getWeights()
            parentWeights1 = self.parents[i+1].getWeights()
            crossoverIndex = randint(0, len(parentWeights0) - 1)
            
            child0Weights = {}
            child1Weights = {}
            j = 0
            for weight in parentWeights0:
                if j < crossoverIndex:
                    child0Weights[weight] = parentWeights0[weight]
                    child1Weights[weight] = parentWeights1[weight]
                else:
                    child0Weights[weight] = parentWeights1[weight]
                    child1Weights[weight] = parentWeights0[weight]
                j+=1

            child0 = Player((childrenNum*self.genNum)+i)
            child1 = Player((childrenNum*self.genNum)+i+1)
            child0.updateWeights(child0Weights)
            child1.updateWeights(child1Weights)
            children += [child0, child1]

        def sortPlayers():
            sortedPlayers = []
            for score in range(21, -22, -1):
                for player in self.players:
                    if player.score == score:
                        sortedPlayers.append(player)
            self.players = sortedPlayers

        
        # Replace the last numParents chromosomes (worst performers) with the new offspring
        sortPlayers()
        numPlayers = len(self.players)
        for j in range(len(children)):
            self.players[numPlayers-j-1] = children[j]
        


    def mutate(self):
        for player in self.players:
            weights = player.getWeights()
            weightKey = sample(set(weights),1)
            newWeights = weights
            newWeights[weightKey[0]] = random()
            player.updateWeights(newWeights)

