#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 23:49:23 2026

@author: simon
"""

def make_floor_plan():
    floor_plan = []
    
    #add x for the isles
    for row in range(7):
        if row == 3:
            floor_plan.append("X" * 80) #80 column
        else:
            floor_plan.append("F" * 80) 
    
    #add S for storage
    for row in [4,5,6]:
        floor_plan[row][76] = "S" #76 and 77 because it starts from 0
        floor_plan[row][77] = "S"
    
    return floor_plan
