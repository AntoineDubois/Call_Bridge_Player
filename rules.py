import numpy as np


def turn(players, order, memory):  # not a good name but "round" is already a default function
    """
    sets a ballot
    Parameters
    ----------
    players : list of 4 strings
        the four players
    order : list of order of players
        order of play
    memory : matrix 4×4×13, dtype int
        matrix of the cards played by the players

    Returns
    -------
    int
        the numero of winner of the round.
        also, it modifies the score of the player
    """
    # load the good model
    players[0].get_model_play(order[0])
    players[1].get_model_play(order[1])
    players[2].get_model_play(order[2])
    players[3].get_model_play(order[3])

    # that block actualizes the memory and plays the cards
    cards = []
    for i in range(4):
        state = memory
        state[order.index(i)] = players[order.index(i)]._hand
        cards.append(players[order.index(i)].playCard(state))
        memory[order.index(i)][cards[-1].card()] = 1

    if (np.array([cards[i]._suit for i in order]) == np.array([0, 0, 0, 0])).any():
        playing0 = [i for i in [0, 1, 2, 3] if cards[i]._suit == 0]
        i = np.argmax([cards[j]._value for j in playing0])
        i = order.index(playing0[i])
        players[i]._score += 1
        players[i]._win = 1
        memory[4, i, 1] += 1
        return i, memory
    else:
        if cards[0]._suit == 1:
            playing1 = [i for i in [0, 1, 2, 3] if cards[i]._suit == 1]
            i = np.argmax([cards[j]._value for j in playing1])
            i = order.index(playing1[i])
            players[i]._score += 1
            players[i]._win = 1
            memory[4, i, 1] += 1
            return i, memory
        elif cards[0]._suit == 2:
            playing2 = [i for i in [0, 1, 2, 3] if cards[i]._suit == 2]
            i = np.argmax([cards[j]._value for j in playing2])
            i = order.index(playing2[i])
            players[i]._score += 1
            players[i]._win = 1
            memory[4, i, 1] += 1
            return i, memory
        else:
            playing3 = [i for i in [0, 1, 2, 3] if cards[i]._suit == 3]
            i = np.argmax([cards[j]._value for j in playing3])
            i = order.index(playing3[i])
            players[i]._score += 1
            players[i]._win = 1
            memory[4, i, 1] += 1
            return i, memory


def scoring(wins, bet):
    """
    computes the score of a player
    Parameters
    ----------
    win : int
        The the number of round won by the player.
    bet : int>0
        The players's expectation.
    Returns
    -------
    The score of the player at the end of a game
    """
    if bet == 0:
        print("A bet is at lest 1")
    elif bet > 13:
        print("A bet can not exceed 13")
    else:
        if bet == wins or bet + 1 == wins:
            if bet > 7:
                return 14
            else:
                return bet
        else:
            if bet > 7:
                return -14
            else:
                return -bet