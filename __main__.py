from player import PlayerStupide, PlayerRandom
from qlearner import Qlearner
from game import Game
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

n = 100

G = Game(players)

G.game(n)

G.plotAverage()
G.plotCumulativeScore()