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

#global variables
booked_seats = [] 
passengers_booked_seats = {} 

#translor row letter into row index number
row_translator = {"A": 0, "B": 1, "C":2, "D":4, "E": 5, "F": 6} 

def check_input(seat_input):
        
    column_string = seat_input[:-1]
    row_letter = seat_input[-1]
        
    #check row is between A to F and column is number
    if not column_string.isdigit() or row_letter not in row_translator:
        print("\nInvalid input. Rows is A-F and column is number of 1-80.(e.g. 1A)\n")
        return #return to keep loop
        
    #check column number is in range of 1 to 80 or not
    col_num = int(column_string)
        
    if col_num < 1 or col_num > 80:
        print("\nInvalid column number. Column should be between 1 to 80.\n")
        return #return to keep loop
        
    #convert row letter and column into python style
    row = row_translator[row_letter]
    column = col_num - 1
    return row, column
    
def option_1(floor_plan):
    print("1. Search by seat coordinate.")
    print("2. Search by passenger name.")
    sec_choice = input("Select an option: ")
    
    if sec_choice == "1":
        seat_input = input("Please enter a seat to check: ").upper().strip()

        row, column = check_input(seat_input)
        
        status = floor_plan[row][column]
        
        if status == "F":
            print(f"\n{seat_input} is available to book.\n")
        elif status == "R":
            print(f"\n{seat_input} is booked.\n")
        elif status == "S":
            print(f"\n{seat_input} is a storage area that cannot be booked.\n")
        elif status == "X":
            print(f"\n{seat_input} is an isles that cannot be booked.\n")
#wait for option 2 and 3 
'''
    if sec_choice == "2":
        name = input("Please enter passenger name: ")
'''
def option_2(floor_plan):
    seat_input = input("Please enter a seat to check: ").upper().strip()
    
    row, column = check_input(seat_input)
    
    status = floor_plan[row][column]
    
    if status == "R":
        print(f"\n{seat_input} is already booked by another passenger.\n")
    elif status == "S":
        print(f"\n{seat_input} is a storage area that cannot be booked.\n")
    elif status == "X":
        print(f"\n{seat_input} is an isles that cannot be booked.\n")
    elif status == "F":
        name = input("Please enter pasenger's name: ").strip().title()
        
        if name == "":
            print("Missing Input. Please try again.")
            return
        
        floor_plan[row][column] = "R"
        
        #save information to global variables
        booked_seats.append(seat_input)
        passengers_booked_seats[name] = seat_input
        
        #success message
        print(f"\n{seat_input} has been booked by {name}.\n")
    

def option_4(floor_plan):
    #summary of booked seats
    print("\nBooked Seats: ", ", ".join(booked_seats),"\n")
    
    print("====================================Burak757 Floor Plan===================================")
    
    #end="" is used to make the output stay in the same sentence
    print("            ",end="") 
    
    for column in range(10,81,10):#frequency of 10 because the output console is too small
        print(column,"       ",end="")
    print()
        
    #making character for every row
    rows = ["A","B","C","X","D","E","F"]
        
    for i in range(7):
        letter = rows[i]
            
        print(letter,"|", end = "") #seperate row character with seat
            
        for seat in floor_plan[i]: #print the seat from the floor plan maked above
            print(seat, end = "")
                
        print()

    print("=" * 90)
    print()

#make main menu
while True: #keep loop till break in option 5
    print("---Apache Airline Seat Booking System---")
    print("1. Check availability of seat")
    print("2. Book a seat")
    print("3. Free a seat")
    print("4. Show booking status")
    print("5. Exit program")
    
    choice = input("Please select an option from 1 to 5: ") #get choice from user
    
    if choice == "1":
        print("\n[Checking availability of seat.]\n")
        option_1(floor_plan)
        
    elif choice == "2":
        print("\n[Booking a seat.]\n")
        option_2(floor_plan)
        
    elif choice == "3":
        print("\n[Freeing a seat.]\n")
        
    elif choice == "4":
        print("\n[Showing floor plan and booking status.]\n")
        option_4(floor_plan)
        
    elif choice == "5":
        print("\n[Exiting program. Thank You for choosing Apache Airlines.]\n")
        break
    else:
        print("\n[Invaild choice. Please input a number (1 - 5).]\n") #for inputs beside 1-5
    
    
    
    
