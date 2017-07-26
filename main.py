import csv
from train import *


def readInData():
	closePrices = []
	dates = []
	with open('SPY.csv') as csvfile:

		reader = csv.reader(csvfile)

		for row in reader:
			date = row[0]
			dates.append(date)
			closePrice = row[5]
			closePrices.append(closePrice)

		# print dates[1:400]
		return closePrices, dates


def main():
	gamma = .99
	learningRate = .05
	epsilon = .1
	init_value = 1000.00
	start = 1
	end = 4000

	SPY_DATA, dates = readInData()

	trainData = SPY_DATA[start:end]

	testData = SPY_DATA[4000:len(SPY_DATA)]

	trainer = Trainer(gamma, learningRate, epsilon, init_value)

	[value, bought, sold, held] = trainer.train(trainData)

	percent = float((value - init_value) / init_value) * 100

	print("Investment: %s, Revenue: %s, Percent Increase: %s , TimePeriod: %s" 
				%('${:,.2f}'.format(init_value), 
					'${:,.2f}'.format(value), 
						'{:,}%'.format(percent), 
							'{:.2f} yrs'.format((end-start + 201)/365)))

	print("Bought: %i, Sold: %i, Held: %i" %(bought, sold, held))



if __name__ == "__main__":
	main()
