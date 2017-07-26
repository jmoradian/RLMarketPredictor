Jordan Moradian
July 26, 2017

RL Market Predictor
-------------------

This is a reinforcement learning approach to predicting the market.
The program, as it is, runs on a very simple reward function that 
returns the difference in portfolio value between the current state
and the previous state. The state feature function contains daily
stock prices of the previous 200 days and the current portfolio value
along with amount of cash in hand. The neural net was built through
tensor flow.
Updates will include optimization of the neural net with respect to
the number of layers involved and the activation functions.# RLMarketPredictor
