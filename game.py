from deck import Deck
from rules import turn, scoring
from NN import save_model_bet, save_model_play
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

class Game:
    def __init__(self, players, learning = False):
        self._players = players
        self._learning = learning
        self._deck = Deck()
        self._memory_hand = np.zeros((4, 4, 13), dtype=int)  # first matrix corresponds to the next player 0

    def initOrder(self):
        self._total_order = [1, 2, 3, 0]

    def initWin(self):
        self._players[0]._win = 0
        self._players[1]._win = 0
        self._players[2]._win = 0
        self._players[3]._win = 0

    def shareDeck(self):
        self._players[0].emptyHand()
        self._players[1].emptyHand()
        self._players[2].emptyHand()
        self._players[3].emptyHand()

        self._deck.shuffleDeck(self._players, self._total_order)

    def showPlayersHands(self):
        return self._players[0]._hand, self._players[1]._hand, self._players[2]._hand, self._players[3]._hand

    def initScore(self):
        self._players[0]._score = 0
        self._players[1]._score = 0
        self._players[2]._score = 0
        self._players[3]._score = 0

    def initScoreHistory(self):
        self._players[0]._history_scores = [0]
        self._players[1]._history_scores = [0]
        self._players[2]._history_scores = [0]
        self._players[3]._history_scores = [0]

    def updateScoreHistory(self):
        self._players[0]._history_scores.append(scoring(self._players[0]._score, self._players[0]._bet))
        self._players[1]._history_scores.append(scoring(self._players[1]._score, self._players[1]._bet))
        self._players[2]._history_scores.append(scoring(self._players[2]._score, self._players[2]._bet))
        self._players[3]._history_scores.append(scoring(self._players[3]._score, self._players[3]._bet))

    def showNames(self):
        print(self._players[0]._name)
        print(self._players[1]._name)
        print(self._players[2]._name)
        print(self._players[3]._name)

    def switchOrder(self):  # automatically chooses the best model
        self._total_order[0], self._total_order[1], self._total_order[2], self._total_order[3] = self._total_order[3], \
                                                                                                 self._total_order[0], \
                                                                                                 self._total_order[1], \
                                                                                                 self._total_order[2]

        self._players[0]._order = self._total_order[0]
        self._players[1]._order = self._total_order[1]
        self._players[2]._order = self._total_order[2]
        self._players[3]._order = self._total_order[3]

        self._players[0].get_model_bet()
        self._players[1].get_model_bet()
        self._players[2].get_model_bet()
        self._players[3].get_model_bet()

    def war(self, change_position=True):
        memory = np.zeros((5, 4, 13), dtype=int)
        order = [self._players[i]._order for i in range(4)]

        self._players_bet = []  # bet block
        for i in range(4):
            self._players_bet.append(self._players[order.index(i)].bet(
                self._players_bet))  # a trick here to tell that player 1 with order 0 players first

        memory[4, :, 0] = self._players_bet

        for k in range(13):  # play cards block
            i, memory = turn(self._players, order, memory)
            if change_position:
                order = order[i:] + order[:i]
            Game.actualizePlay(self, memory, k)
            Game.initWin(self)

    def game(self, n=1, change_position=True):
        """
        realises n number of games

        Parameters
        ----------
        n : int
            The number of games to be realised
        change_position : bool
            whether the winer should play first
        computes
        -------
        the historic of players' scores

        """
        self._n = n
        Game.initScoreHistory(self)
        Game.initOrder(self)
        for i in tqdm(range(1, self._n + 1), ascii=False, unit="game"):
            Game.actualizeLearningRate(self, i)
            Game.switchOrder(self)
            Game.initScore(self)
            Game.shareDeck(self)
            Game.war(self, change_position=True)
            Game.updateScoreHistory(self)
            Game.actualizeBet(self)
            if i % 100 == 0:
                Game.save_models(self)
        Game.save_models(self)

    def actualizeBet(self):  # players compare their bet and their score
        self._players[0].actualize_bet(self._learning)
        self._players[1].actualize_bet(self._learning)
        self._players[2].actualize_bet(self._learning)
        self._players[3].actualize_bet(self._learning)

    def actualizePlay(self, memory, game_round):
        for i in range(4):
            new_state = memory
            new_state[i] = self._players[i]._hand
            self._players[i].actualize_play(new_state, game_round, self._learning)

    def actualizeLearningRate(self, round_nb):

        if self._learning:
            self._players[0]._epsilon = (1 + round_nb)**(-0.45)
            self._players[1]._epsilon = (1 + round_nb)**(-0.45)
            self._players[2]._epsilon = (1 + round_nb)**(-0.45)
            self._players[3]._epsilon = (1 + round_nb)**(-0.45)
        else:
            self._players[0]._epsilon = 0
            self._players[1]._epsilon = 0
            self._players[2]._epsilon = 0
            self._players[3]._epsilon = 0

    def save_models(self):
        if self._learning:
            save_model_bet()
            save_model_play()

    def showScores(self):
        for k in range(4):
            self._players[k].showScore()

    def showHistory(self):
        dic_history = {}
        dic_history[self._players[0]._name] = self._players[0].historyScore()
        dic_history[self._players[1]._name] = self._players[1].historyScore()
        dic_history[self._players[2]._name] = self._players[2].historyScore()
        dic_history[self._players[3]._name] = self._players[3].historyScore()
        return dic_history

    def plotAverage(self):
        dic_history = Game.showHistory(self)
        average = []
        for i in range(self._n + 1):
            average.append((dic_history[self._players[0]._name][i] + dic_history[self._players[1]._name][i] +
                            dic_history[self._players[2]._name][i] + dic_history[self._players[3]._name][i]) / 4)
        plt.plot(list(range(self._n + 1)), average, label="Score average")
        plt.plot(list(range(self._n + 1)), dic_history[self._players[0]._name], label=self._players[0]._name)
        plt.plot(list(range(self._n + 1)), dic_history[self._players[1]._name], label=self._players[1]._name)
        plt.plot(list(range(self._n + 1)), dic_history[self._players[2]._name], label=self._players[2]._name)
        plt.plot(list(range(self._n + 1)), dic_history[self._players[3]._name], label=self._players[3]._name)
        plt.legend()
        plt.title("Scores")
        plt.show()

    def plotScores(self):
        dic_history = Game.showHistory(self)
        plt.plot(list(range(self._n + 1)), dic_history[self._players[0]._name], label=self._players[0]._name)
        plt.plot(list(range(self._n + 1)), dic_history[self._players[1]._name], label=self._players[1]._name)
        plt.plot(list(range(self._n + 1)), dic_history[self._players[2]._name], label=self._players[2]._name)
        plt.plot(list(range(self._n + 1)), dic_history[self._players[3]._name], label=self._players[3]._name)
        plt.legend()
        plt.title("Scores")
        plt.show()

    def cumulativeScore(self):
        dic_cumulative_history = Game.showHistory(self)
        dic_cumulative_history[self._players[0]._name] = kahan_cumsum(self._players[0].historyScore())
        dic_cumulative_history[self._players[1]._name] = kahan_cumsum(self._players[1].historyScore())
        dic_cumulative_history[self._players[2]._name] = kahan_cumsum(self._players[2].historyScore())
        dic_cumulative_history[self._players[3]._name] = kahan_cumsum(self._players[3].historyScore())
        return dic_cumulative_history

    def plotCumulativeScore(self):
        dic_cumulative_history = Game.cumulativeScore(self)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history[self._players[0]._name], label=self._players[0]._name)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history[self._players[1]._name], label=self._players[1]._name)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history[self._players[2]._name], label=self._players[2]._name)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history[self._players[3]._name], label=self._players[3]._name)
        plt.legend()
        plt.title("Cumulative scores")
        plt.show()

    def cumulativeScore_neg(self):
        dic_cumulative_history_neg = Game.showHistory(self)
        dic_cumulative_history_neg[self._players[0]._name] = kahan_cumsum_neg(self._players[0].historyScore())
        dic_cumulative_history_neg[self._players[1]._name] = kahan_cumsum_neg(self._players[1].historyScore())
        dic_cumulative_history_neg[self._players[2]._name] = kahan_cumsum_neg(self._players[2].historyScore())
        dic_cumulative_history_neg[self._players[3]._name] = kahan_cumsum_neg(self._players[3].historyScore())
        return dic_cumulative_history_neg

    def plotCumulativeScore_neg(self):
        dic_cumulative_history_neg = Game.cumulativeScore_neg(self)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history_neg[self._players[0]._name], label=self._players[0]._name)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history_neg[self._players[1]._name], label=self._players[1]._name)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history_neg[self._players[2]._name], label=self._players[2]._name)
        plt.plot(list(range(self._n + 1)), dic_cumulative_history_neg[self._players[3]._name], label=self._players[3]._name)
        plt.legend()
        plt.title("Cumulative scores neg")
        plt.show()


def kahan_cumsum(x):
    x = np.asarray(x)
    cumulator = np.zeros_like(x)
    cumulator[0] = x[0]
    for i in range(1, len(x)):
        cumulator[i] = max(x[i] + x[i - 1], 0)
    return cumulator

def kahan_cumsum_neg(x):
    x = np.asarray(x)
    cumulator = np.zeros_like(x)
    cumulator[0] = x[0]
    for i in range(1, len(x)):
        cumulator[i] = x[i] + x[i - 1]
    return cumulator