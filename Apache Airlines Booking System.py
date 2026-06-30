#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 23:49:23 2026

@author: simon
"""
import random
import string
import sqlite3

class Apache_airline_Burak757_booking_system:
    def __init__(self):
        self.db = "apache_airline_Burak757.db"
        #translor row letter into row index number
        self.row_translator = {"A": 0, "B": 1, "C":2, "D":4, "E": 5, "F": 6} 

        self.booked_seats = [] 
        self.floor_plan = self.make_floor_plan()
        self.init_database()
        
    def init_database(self):
        #connect to db
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        #reference is the unique primary key
        #passport_num is text since it may combine with letter and digits
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers_booked_seats (
            reference TEXT PRIMARY KEY,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            passport_num TEXT NOT NULL,
            row TEXT NOT NULL,
            column INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def booking_reference(self):
        
        #from builtin string, gets all letter and digits and save it into variable
        all_characters = string.ascii_uppercase + string.digits
        #connect to db
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        while True:
            #builtin random is used to randomly choose 8 elements from k, .join to store into a string
            test_reference = ''.join(random.choices(all_characters,k=8))#k is the length of elemnets 
            cursor.execute("SELECT 1 FROM passengers_booked_seats WHERE reference = ?", (test_reference,)) #comma is used to make it a tuple
            #fetchone() means taking the result from the db
            if cursor.fetchone() is None: #if NONE means it is unique
                conn.close()
                return test_reference          
    
    def make_floor_plan(self):
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
    
    def check_input(self, seat_input):
            
        column_string = seat_input[:-1]
        row_letter = seat_input[-1]
            
        #check row is between A to F and column is number
        if not column_string.isdigit() or row_letter not in self.row_translator:
            print("\nInvalid input. Rows is A-F and column is number of 1-80.(e.g. 1A)\n")
            #two None is used to prevent error
            return None, None #return to keep loop
            
        #check column number is in range of 1 to 80 or not
        col_num = int(column_string)
            
        if col_num < 1 or col_num > 80:
            print("\nInvalid column number. Column should be between 1 to 80.\n")
            return None, None #return to keep loop
            
        #convert row letter and column into python style
        row = self.row_translator[row_letter]
        column = col_num - 1
        return row, column
        
    def cal_seat_price(self,row_letter,col_num):
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
        
    
    def option_1(self):
        print("1. Search by seat coordinate.")
        print("2. Search by passenger name.")
        sec_choice = input("Select an option: ")
        
        if sec_choice == "1":
            seat_input = input("Please enter a seat to check: ").upper().strip()
    
            row, column = self.check_input(seat_input)
            
            if row is None:
                return
            
            status = self.floor_plan[row][column]
            
            if status == "F":
                print(f"\n{seat_input} is available to book.\n")
            elif status not in ["F", "S", "X"]: #Because R is changed into reference number
                print(f"\n{seat_input} is booked.\n")
            elif status == "S":
                print(f"\n{seat_input} is a storage area that cannot be booked.\n")
            elif status == "X":
                print(f"\n{seat_input} is an isles that cannot be booked.\n")
    
        elif sec_choice == "2":
            #strip() used to remove unnessacry space
            #title() used to upper the first character of the name
            first_name = input("Please enter passenger's First Name: ").strip().title()
            last_name = input("Please enter passenger's Last Name: ").strip().title()
            
            #connect to db
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            
            #get data from db to find matches 
            #? as variables, then give the value of it in the later ()
            cursor.execute("SELECT column,row FROM passengers_booked_seats WHERE firstname = ? AND lastname = ?", (first_name, last_name))
            
            all_bookings = cursor.fetchall() #take all bookings of that guy
            conn.close()
            
            if len(all_bookings) > 0:
                #joining seats into a clean format
                booking_list = ", ".join(f"{seat[0]}{seat[1]}" for seat in all_bookings)
                print(f"\n{first_name}{last_name} has boked seat(s): {booking_list}.\n")
            else:
                print("\nNo bookings were found.\n")

        else:
            print("\nInvalid Option. Please try again with option 1 and 2.\n")
            return 

    def option_2(self):
        seat_input = input("Please enter a seat to book: ").upper().strip()
        
        row, column = self.check_input(seat_input)
        if row is None:
            return
        
        status = self.floor_plan[row][column]
        
        if status not in ["F", "S", "X"]: #Because R is changed into reference number
            print(f"\n{seat_input} is already booked by another passenger.\n")
        elif status == "S":
            print(f"\n{seat_input} is a storage area that cannot be booked.\n")
        elif status == "X":
            print(f"\n{seat_input} is an isles that cannot be booked.\n")
        elif status == "F":
            row_letter = seat_input[-1]
            col_num = int(seat_input[:-1])
            
            print(f"\n{seat_input} is free to book.")
            ticket_price = self.cal_seat_price(row_letter, col_num)
            print(f"Price of {seat_input} is £{ticket_price}.\n")
            
            first_name = input("Please enter pasenger's First Name: ").strip().title()
            last_name = input("Please enter pasenger's Last Name: ").strip().title()
            passport = input("Please enter pasenger's Passport Number: ").strip().upper()
            
            if first_name == "" or last_name == "" or passport == "":
                print("\nThere are missing Input. Please try again.\n")
                return
            
            ref = self.booking_reference()
            
            #connect to db
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            
            #insert that passengers detail into db
            cursor.execute('''
                           INSERT INTO passengers_booked_seats(
                               reference, firstname, lastname, passport_num, row, column)
                           VALUES (?,?,?,?,?,?)
                           ''', 
                           (ref, first_name, last_name, passport, row_letter, col_num)
                           )
            
            conn.commit()
            conn.close()
            

            #change that coordinate to reference
            self.floor_plan[row][column] = ref
            
            #save information to global variables
            self.booked_seats.append(seat_input.upper().strip())
                        
            #success message
            print(f"\n{seat_input} has been booked by {first_name} {last_name}.\n")
            print(f"Reference of this booking is: {ref}\n")
            
    def option_3(self):
        seat_input = input("Please enter a seat to free: ").upper().strip()
        
        row, column = self.check_input(seat_input)    
        if row is None:
            return
            
        status = self.floor_plan[row][column]
        
        if status == "F":
            print(f"\n{seat_input} is already free.\n")
        elif status == "S":
            print(f"\n{seat_input} is a storage area that cannot be booked.\n")
        elif status == "X":
            print(f"\n{seat_input} is an isles that cannot be booked.\n")
            
        else: #since the status is not R anymore
            print(f"The seat has booked with the booking reference: {status}")
            #check it by passport number instead of name
            check_passport = input("Please enter passenger's Passport Number to canel booking: ").strip.upper()
            
            #connect to db
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            
            cursor.execute("SELECT firstname, lastname FROM passengers_booked_seats WHERE reference = ? AND passport_num = ?", (status, check_passport))
            passenger = cursor.fetchone()
            
            if passenger is None:
                print("\nError. Passport number does not match.\n")
                conn.close()
                return 
            
            first_name, last_name = passenger
            #delete the data from db
            cursor.execute("DELETE FROM passengers_booked_seats WHERE reference = ?", (status))
            conn.commit()
            conn.close()
            

            #change that coordinate to free
            self.floor_plan[row][column] = "F"
            
            if seat_input in self.booked_seats:
                self.booked_seats.remove(seat_input)
            
                
            print(f"\nBooking of {seat_input} has remove from {first_name} {last_name}.\n")
    
    def option_4(self):
        #summary of booked seats
        print("\nBooked Seats: ", ", ".join(self.booked_seats),"\n")
        
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
                
            for seat in self.floor_plan[i]: #print the seat from the floor plan maked above
                #change the Reference back to R since it will break the layout of the floor plan
                if len(seat) == 8: 
                    print("R", end = "")
                else:    
                    print(seat, end = "")
                    
            print()
    
        print("=" * 90)
        print()
    
    def run(self):
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
                self.option_1()
                
            elif choice == "2":
                print("\n[Booking a seat.]\n")
                self.option_2()
                
            elif choice == "3":
                print("\n[Freeing a seat.]\n")
                self.option_3()
                
            elif choice == "4":
                print("\n[Showing floor plan and booking status.]\n")
                self.option_4()
                
            elif choice == "5":
                print("\n[Exiting program. Thank You for choosing Apache Airlines.]\n")
                break
            else:
                print("\n[Invalid choice. Please input a number (1 - 5).]\n") #for inputs beside 1-5

if __name__ == "__main__":
    app = Apache_airline_Burak757_booking_system()
    app.run()
    
    
    
    