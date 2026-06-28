#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 23:49:23 2026

@author: simon
"""
import random
import string

reference = set()
def booking_reference():
    
    #from builtin string, gets all letter and digits and save it into variable
    all_characters = string.ascii_uppercase + string.digits
    
    while True:
        #builtin random is used to randomly choose 8 elements from k, .join to store into a string
        test_reference = ''.join(random.choice(all_characters,k=8))#k is the length of elemnets 
        
        if test_reference not in reference:
            reference.add(test_reference)
            return test_reference
        

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
        #two None is used to prevent error
        return None, None #return to keep loop
        
    #check column number is in range of 1 to 80 or not
    col_num = int(column_string)
        
    if col_num < 1 or col_num > 80:
        print("\nInvalid column number. Column should be between 1 to 80.\n")
        return None, None #return to keep loop
        
    #convert row letter and column into python style
    row = row_translator[row_letter]
    column = col_num - 1
    return row, column
    
def cal_seat_price(row_letter,col_num):
    #using row as letter to look through storage
    if row_letter in ['D', 'E', 'F'] and col_num in [77,78]:
        return 0 
    if row_letter == 'X':
        return 0
    
    if 1 <= col_num <= 3:
        return 250
    elif 4 <= col_num <= 5:
        return 200
    else:
        return 100
    

def option_1(floor_plan):
    print("1. Search by seat coordinate.")
    print("2. Search by passenger name.")
    sec_choice = input("Select an option: ")
    
    if sec_choice == "1":
        seat_input = input("Please enter a seat to check: ").upper().strip()

        row, column = check_input(seat_input)
        
        if row is None:
            return
        
        status = floor_plan[row][column]
        
        if status == "F":
            print(f"\n{seat_input} is available to book.\n")
        elif status == "R":
            print(f"\n{seat_input} is booked.\n")
        elif status == "S":
            print(f"\n{seat_input} is a storage area that cannot be booked.\n")
        elif status == "X":
            print(f"\n{seat_input} is an isles that cannot be booked.\n")

    elif sec_choice == "2":
        #strip() used to remove unnessacry space
        #title() used to upper the first character of the name
        name = input("Please enter passenger name: ").strip().title() 
        
        if name in passengers_booked_seats:
            booked_list = passengers_booked_seats[name]
            clean_list = ", ".join(booked_list)
            
            print(f"\n{name} has booked seat(s): {clean_list}.\n")
        else:
            print("\nNo bookings were found.\n")
    else:
        print("\nInvalid Option. Please try again with option 1 and 2.\n")
        return 

def option_2(floor_plan):
    seat_input = input("Please enter a seat to book: ").upper().strip()
    
    row, column = check_input(seat_input)
    if row is None:
        return
    
    status = floor_plan[row][column]
    
    if status == "R":
        print(f"\n{seat_input} is already booked by another passenger.\n")
    elif status == "S":
        print(f"\n{seat_input} is a storage area that cannot be booked.\n")
    elif status == "X":
        print(f"\n{seat_input} is an isles that cannot be booked.\n")
    elif status == "F":
        row_letter = seat_input[-1]
        col_num = int(seat_input[:-1])
        
        ticket_price = cal_seat_price(row_letter, col_num)
        print(f"\nPrice of {seat_input} is £{ticket_price}.\n")
        
        name = input("Please enter pasenger's name: ").strip().title()
        
        if name == "":
            print("\nMissing Input. Please try again.\n")
            return
        
        #change that coordinate to booked
        floor_plan[row][column] = "R"
        
        #save information to global variables
        booked_seats.append(seat_input.upper().strip())
        
        if name in passengers_booked_seats:
            passengers_booked_seats[name].append(seat_input.upper().strip())
        else:#create a list if no booking are done before
            passengers_booked_seats[name] = [seat_input.upper().strip()]
        
        #success message
        print(f"\n{seat_input} has been booked by {name}.\n")
        
def option_3(floor_plan):
    seat_input = input("Please enter a seat to free: ").upper().strip()
    
    row, column = check_input(seat_input)    
    if row is None:
        return
        
    status = floor_plan[row][column]
    
    if status == "F":
        print(f"\n{seat_input} is already free.\n")
    elif status == "S":
        print(f"\n{seat_input} is a storage area that cannot be booked.\n")
    elif status == "X":
        print(f"\n{seat_input} is an isles that cannot be booked.\n")
    elif status == "R":
        name = input(f"Please enter pasenger's name that book {seat_input}: ").strip().title()
        
        if name not in passengers_booked_seats or seat_input not in passengers_booked_seats[name]:
            print(f"\nError. {name} did not book {seat_input}.\n")
            return
        
        if name == "":
            print("\nMissing Input. Please try again.\n")
            return
        #change that coordinate to free
        floor_plan[row][column] = "F"
        
        if seat_input in booked_seats:
            booked_seats.remove(seat_input)
        
        passengers_booked_seats[name].remove(seat_input)
        
        if len(passengers_booked_seats[name]) == 0:
            del passengers_booked_seats[name]
            
        print(f"\nBooking of {seat_input} has remove from {name}.\n")

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
    print("4. Show floor plan & booking status")
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
        option_3(floor_plan)
        
    elif choice == "4":
        print("\n[Showing floor plan and booking status.]\n")
        option_4(floor_plan)
        
    elif choice == "5":
        print("\n[Exiting program. Thank You for choosing Apache Airlines.]\n")
        break
    else:
        print("\n[Invalid choice. Please input a number (1 - 5).]\n") #for inputs beside 1-5
    
    
    
    
