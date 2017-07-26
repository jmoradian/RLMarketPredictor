import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np

from reward import *
from portfolio import *
from state import *


# uses a 3 layer neural net with two relu activation functions and a final 
# softmax function
class Trainer(object):

	def __init__(self, gamma, learningRate, epsilon, init_value):
		# setting up the network
		self.gamma = gamma
		self.learningRate = learningRate
		self.epsilon = epsilon


		self.X = tf.placeholder(shape=[1, 203],dtype=tf.float32)

		self.W1 = tf.Variable(tf.zeros([203, 75]))
		self.W2 = tf.Variable(tf.zeros([75, 15]))
		self.W3 = tf.Variable(tf.zeros([15, 3]))

		self.B1 = tf.Variable(tf.zeros([75]))
		self.B2 = tf.Variable(tf.zeros([15]))
		self.B3 = tf.Variable(tf.zeros([3]))

		self.init = tf.global_variables_initializer()

		self.Y1 = tf.nn.relu(tf.matmul(self.X, self.W1) + self.B1)
		self.Y2 = tf.nn.relu(tf.matmul(self.Y1, self.W2) + self.B2)
		self.Y3 = tf.nn.softmax(tf.matmul(self.Y2, self.W3) + self.B3)
		self.prediction = tf.argmax(self.Y3, 1)
		self.optimal_q_value = tf.placeholder(tf.float32)

		# the loss function
		self.Qprime = tf.placeholder(shape=[1,3],dtype=tf.float32)
		self.r = tf.placeholder(tf.float32)
	

		# self.loss = tf.reduce_sum(tf.square(self.Qprime - self.Y3))
		self.QprimeInd = tf.placeholder(tf.int32)
		self.Qadj = self.gamma * self.Qprime + self.r
		# reward function has no affect on this for some reason
		self.squared_error = tf.square(self.Qadj - self.Y3)
		self.sum_squared_error = tf.reduce_sum(self.squared_error)
		self.loss = tf.reduce_mean(self.sum_squared_error)

		self.trainer = tf.train.GradientDescentOptimizer(learning_rate=learningRate)
		self.updateModel = self.trainer.minimize(self.squared_error)

		self.portfolio = Portfolio(init_value)
		self.stateGenerator = State(self.portfolio)
		self.reward = Reward(self.stateGenerator)


	def train(self, trainData):

		bought = 0
		sold = 0
		held = 0

		sess = tf.Session()
		sess.run(self.init)

		# This produces just one learning episode
		for timestep in range(201, len(trainData) - 1):
			# generates the batch for this training step
			state = self.stateGenerator.generateStateFeatures(trainData, timestep)
			batch = {self.X: state}
			

			# get optimal action and execute
			action, Qvalues = sess.run([self.prediction, self.Y3], feed_dict = batch)
			Qvalue = Qvalues[0][action[0]]

			#chance of random action
			if np.random.rand(1) < self.epsilon:
				action = self.stateGenerator.chooseRandomAction(state)

			if (action == [0]):
				# print "BUY"
				bought += 1
			elif (action == [1]):
				# print "SELL"
				sold += 1
			elif (action == [2]):
				# print "HOLD"
				held += 1

			# print action
			self.stateGenerator.executeAction(state, action)

			# get next state and reward
			sprime = self.stateGenerator.generateStateFeatures(trainData, timestep + 1)
			reward = self.reward.rewardFunction(state, action, sprime)

			nextBatch = {self.X: sprime}
			aprime, Qprime = sess.run([self.prediction, self.Y3], feed_dict = batch)

			QprimeInd = Qprime[0][aprime[0]]


			QprimeBatch = {self.Qprime: Qprime, self.X: state, 
							self.QprimeInd: QprimeInd, self.r: reward, 
							self.optimal_q_value: Qvalue}
			sess.run(self.updateModel, feed_dict = QprimeBatch)

		return [self.stateGenerator.getPortfolioValue(state), bought, sold, held]





















