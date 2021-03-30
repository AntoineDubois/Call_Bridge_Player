#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:05:34 2021

@author: duboisantoine
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:45:05 2021

@author: duboisantoine
"""
from player import Player
from deck import Card
from NN import model_bet, model_play
from rules import scoring
import numpy as np


class Qlearner(Player):
    def __init__(self, name):
        Player.__init__(self, name)
            
        self._gamma = 0.9
        self._epsilon = 0.1
        
        
    def get_model_bet(self):
        self._model_bet = model_bet[self._order]
    
    def get_model_play(self, order):
        self._model_play = model_play[order]
    
    def bet(self, others_bet):
        self._init_hand = np.reshape(self._hand, 52)
        self._init_hand_bet = np.concatenate((self._init_hand, np.array(others_bet)), axis = 0)
        self._bet = np.argmax(self._model_bet.predict(np.array([self._init_hand_bet]))) 
        if self._bet == 0:
            self._bet += 1
            return self._bet
        else:
            self._bet = min(7, self._bet)
            return self._bet
        
        
    def actualize_bet(self):
        self._model_bet.fit(np.array([self._init_hand_bet]), np.array([self._score]), epochs=1, verbose=0)
        
        
    def playCardRandom(self, *ards): #the player plays a random card of his hand
        a,b = np.where(self._hand == 1)
        that_card = np.random.randint(len(a))
        suit, value = a[that_card], b[that_card]
        self._hand[suit, value] = 0
        return (suit, value)
    
    
    def playCard(self, state):
        self._memory = state
        if np.random.rand() < self._epsilon:
            self._action = Qlearner.playCardRandom(self)
        else:
            a = np.reshape(self._memory, 260)
            Q = self._model_play.predict(np.array([a]))
            Q = np.reshape(Q, (4,13))# Q-values predictions
            Q[self._hand == 0] = Q.min()   #avoid a non owned card be played
            suit, value = np.unravel_index(Q.argmax(), Q.shape)     # Move with highest Q-value is the chosen one
            self._hand[suit, value] = 0
            self._action = (suit, value)
        return Card(self._action[0], self._action[1])

    def actualize_play(self, new_state, game_round):#end is  if at round 13
        #self._win tells whether the player has wone the last round
        a = np.reshape(self._memory, 260)
        target = self._model_play.predict(np.array([a]))    
        
        if game_round == 13:
            #target = scoring(self._score, self._bet)
            target[0, (self._action[0]+1)*self._action[1]] = scoring(self._score, self._bet)
        else:
            b = np.reshape(new_state, 260)
            maxQ = np.max(self._model_play.predict(np.array([b])))
            
            target[0, (self._action[0]+1)*self._action[1]] = self._win + self._gamma * maxQ
            
        target = np.reshape(target, 52)
        
        self._model_play.fit(np.array([a]), np.array([target]), verbose=False)