
from state import *


class Reward():
	def __init__(self, stateGenerator):
		self.stateGenerator = stateGenerator

	def differencePortfolioValue(self, state, sprime):
		prevPortfolioValue = float(self.stateGenerator.getPortfolioValue(state))
		currPortfolioValue = float(self.stateGenerator.getPortfolioValue(sprime))

		return float((currPortfolioValue - prevPortfolioValue))

	def differenceCash(self, state, sprime):
		prevCashAmount = float(self.stateGenerator.getCash(state))
		currCashAmount = float(self.stateGenerator.getCash(sprime))

		return float((currCashAmount - prevCashAmount))

	def rewardFunction(self, s, a, sprime):
		r = self.differencePortfolioValue(s, sprime)
		return r
