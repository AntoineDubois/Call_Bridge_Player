from player import PlayerStupide, PlayerRandom
from Qlearner import Qlearner
from game import Game
import numpy as np
#===========================
"""
bob = PlayerStupide("Bob") 
joe = PlayerStupide("Joe")
leo = PlayerStupide("Leo")
sam = PlayerStupide("Sam")
players=[bob,joe,leo,sam]
n = 10
G = Game(players)
G.game(n)
G.plotAverage()
G.plotCumulativeScore()
#===========================
bob = PlayerRandom("Bob") 
joe = PlayerRandom("Joe")
leo = PlayerRandom("Leo")
sam = PlayerRandom("Sam")
players=[bob,joe,leo,sam]
n = 10
G = Game(players)
G.game(n)
G.plotAverage()
G.plotCumulativeScore()"""

#===========================

bob = Qlearner("Bob") 
joe = Qlearner("Joe")
leo = Qlearner("Leo")
sam = Qlearner("Sam")
players=[bob,joe,leo,sam]

n = 10
G = Game(players, learning=True)

G.game(n)

G.plotAverage()
G.plotCumulativeScore()
G.plotCumulativeScore_neg()

print("Bob's average", np.average(G.showHistory()["Bob"]))
print("Joe's average", np.average(G.showHistory()["Joe"]))
print("Leo's average", np.average(G.showHistory()["Leo"]))
print("Sam's average", np.average(G.showHistory()["Sam"]))