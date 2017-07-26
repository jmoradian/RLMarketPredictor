


class Portfolio():

	def __init__(self, init_value):
		self.numberOfShares = 0
		self.valueOfAssets = 0.00
		self.cash = init_value
		self.totalPortfolioValue = init_value

	def getNumAssets(self):
		return float(self.numberOfShares)

	def setNumAssets(self, numAssets, sharePrice):
		self.numberOfShares = float(numAssets)
		self.setValueOfAssets(sharePrice)

	def setValueOfAssets(self, sharePrice):
		self.valueOfAssets = float(self.numberOfShares) * float(sharePrice)
		self.totalPortfolioValue = self.valueOfAssets + self.cash

	def getAmountLiquid(self):
		return self.cash

	def setCash(self, amountCash):
		self.cash = amountCash
		self.totalPortfolioValue = self.valueOfAssets + self.cash

	def getTotalPortfolioValue(self, value):
		return self.totalPortfolioValue