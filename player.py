#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 17:58:14 2020

@author: duboisantoine
"""
import random
from deck import Card
import numpy as np
    
class Player: 
    def __init__(self, name): 
        self._name = name 
        self._hand = np.zeros((4,13), dtype=int) 
        self._bet = 0
        self._score = 0
        self._history_scores = [self._score]
        self._order = None
        self._win = 0
        
        #to save memory, you assume the memory of played cards as common. In consequence, the memory is stored in Game
        #self._memory_bet = []
        #self._memory_hand = np.zeros((3,4,13), dtype=int) #first matrix correspond to the next player
        
        
    def numberCards(self):
        return np.sum(self._hand)
        
    def emptyHand(self):
        self._hand = np.zeros((4,13), dtype=int)
    
    def showHand(self): 
        for i in range(4):
            for j in range(13):
                if self._hand[i,j]:
                    print(Card(i, j).show())

    def showScore(self):
         print(self._score)
         
    def registerScore(self):#convenient but slow
        self._history_scores.append(self._score)
    
    def historyScore(self):
        return self._history_scores
    
    def actualize_bet(self, *arg):
        pass
    
    def actualize_play(self, *arg):
        pass
    
    def get_model_bet(self):
        pass
    
    def get_model_play(self, *arg):
        pass
    
    
         
class PlayerStupide(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def bet(self, others_bet = None):
        self._bet = 7
        return self._bet
    
    def playCard(self, *args): #the player plays the first card of his hand        
        suits, values = np.where(self._hand == 1)
        self._hand[suits[0], values[0]] = 0
        return Card(suits[0], values[0])
    
    

class PlayerRandom(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def bet(self, others_bet = None):
        self._bet = random.randint(1, 13)
        return self._bet
    
    def playCard(self, *args): #the player plays a random card of his hand
        a,b = np.where(self._hand == 1)
        that_card = np.random.randint(len(a))
        suit, value = a[that_card], b[that_card]
        self._hand[suit, value] = 0
        return Card(suit, value)