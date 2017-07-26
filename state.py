import numpy as np
import random

from portfolio import *


class State():

	def __init__(self, portfolio):
		self.features = []
		self.portfolio = portfolio

	def generateFeatureMatrix(self, data):
		featureMatrix = []
		for i in range(201, len(data)):
				featureMatrix.append(data[i-200: i])

		return featureMatrix

	# returns feature vector of a single state
	def generateStateFeatures(self, data, timestep):
		features = [self.portfolio.totalPortfolioValue, 
					self.portfolio.numberOfShares, 
					self.portfolio.cash]
		self.features = np.array([features + data[timestep - 200: timestep]])
		return self.features

	def getPortfolioValue(self, state):
		return float(state[0][0])

	def getCash(self, state):
		return float(state[0][2])

	def getSharePrice(self, state):
		return float(state[0][len(state[0]) - 1])


		# 0 is hold; 1 is sell; 2 is buy
	def executeAction(self, state, action):
		numShares = 1
		sharePrice = self.getSharePrice(state)

		# buy action
		if (action[0] == 2 and self.portfolio.cash > sharePrice):
			self.portfolio.setCash(self.portfolio.cash - sharePrice * numShares)
			self.portfolio.setNumAssets(self.portfolio.numberOfShares + 1, sharePrice)
			self.portfolio.setValueOfAssets(sharePrice)
		# sell action
		elif (action[0] == 1 and self.portfolio.numberOfShares != 0):
			self.portfolio.setNumAssets(self.portfolio.numberOfShares - 1, sharePrice)
			self.portfolio.setCash(self.portfolio.cash + sharePrice * numShares)
			self.portfolio.setValueOfAssets(sharePrice)
		# hold action
		else:
			self.portfolio.setValueOfAssets(sharePrice)


	def chooseRandomAction(self, state):
		return random.choice([[0],[1],[2]])








