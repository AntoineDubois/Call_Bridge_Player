#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 18:27:34 2020

@author: duboisantoine
"""
import numpy as np

class Card: 
    def __init__(self, suit, value): 
        self._value = value 
        self._suit = suit 
    
    def card(self):
        return (self._suit, self._value)
    
    def show(self):#we call that function applied on a class a methode 
        suits = ["Spade", "Club", "Diamond", "Heart"]
        values = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        print(values[self._value], "of", suits[self._suit])
        return ""
 
"""
Spade: 0
Club: 1
Diamond: 2
Heart: 3
Avoiding letters is way faster
"""

class Deck: 
    def __init__(self): 
        self._deck = np.ones(( 4, 13), dtype=int)
    def shuffleDeck(self, players, order):
        self._deck = np.ones(( 4, 13), dtype=int)
        for i in order:
            while np.sum(players[i]._hand) < 13:
                a, b = np.random.randint(4), np.random.randint(13)
                if self._deck[a,b] :
                    players[i]._hand[a,b] = 1
                    self._deck[a,b] = 0