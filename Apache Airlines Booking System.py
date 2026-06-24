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
            floor_plan.append(["X"] * 80) #80 column
        else:
            floor_plan.append(["F"] * 80) 
    
    #add S for storage
    for row in [4,5,6]:
        floor_plan[row][76] = "S" #76 and 77 because it starts from 0
        floor_plan[row][77] = "S"
    
    return floor_plan
floor_plan = make_floor_plan()

#make main menu
while True:
    print("---Apache Airline Seat Booking System---")
    print("1. Check availability of seat")
    print("2. Book a seat")
    print("3. Free a seat")
    print("4. Show booking status")
    print("5. Exit program")
    
    choice = input("Please select an option from 1 to 5: ")
    
    if choice == "1":
        print("\n[Checking availability of seat.]\n")
        
    elif choice == "2":
        print("\n[Booking a seat.]\n")
        
    elif choice == "3":
        print("\n[Freeing a seat.]\n")
        
    elif choice == "4":
        print("\n[Showing booking status.]\n")
        
    elif choice == "5":
        print("\n[Exiting program. Thank You for choosing Apache Airlines.]\n")
        break
    else:
        print("\n[Invaild choice. Please input a number (1 - 5).]\n")