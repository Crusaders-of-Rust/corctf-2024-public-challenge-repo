#!/usr/bin/env python
import time
import sys

print("Hello agent. Thanks for your hard work in the field researching. We'll now ask you 6 questions on the information you've gathered.")
sys.stdout.flush()


print("I'd like to take this opportunity to remind you that our targets are located in the United Kingdom, so their timezone is BST (UTC +1).")

question1 = input("We'd like to confirm what the username of the main user on the target's computer is. Can you provide this information? ")

if question1 == "slice1":
    print("Correct! Excellent work.")
else:
    print("Incorrect. Please try again next time!") 
    exit()


question2 = input("Now, we'd like the name of the computer, after it was renamed. Ensure that it is entered in exactly how it is in the logs. ")

if question2 == "lemon-squeezer":
    print("Correct! Excellent work.")
    print("I wonder if they'll make any lemonade with that lemon-squeezer...")
else:
    print("Incorrect. Please try again next time!") 
    exit()


question3 = input("Great work! In order to prevent their lemons from moulding, the lemonthinkers changed the maximum password age. What is this value? Please enter it as an integer number in days. ")

if question3 == "83":
    print("Correct! Excellent work.")
else:
    print("Incorrect. Please try again next time!") 
    exit()


question4 = input("It seems that our targets are incredibly smart, and turned off the antivirus. At what time did this happen? Give your answer as a UNIX timestamp. ")

if question4.isdigit():
    if abs(int(question4) - 1721946080) < 100:
        print("Correct! Excellent work.")
    else:
        print("Incorrect. Please try again next time!") 
        exit()
else:
    print("I think that UNIX timestamps are generally integer numbers....")
    exit()

question5 = input("The main lemonthinker, slice1, hasn't learnt from the-conspiracy and has (again) downloaded some malware on the system. What is the name of the user created by this malware? ")

if question5 == "notabackdoor":
    print("Correct! Excellent work.")
else:
    print("Incorrect. Please try again next time!") 
    exit()

question6 = input("Finally, we'd like to know the name of the group that the user created by the malware is part of, which has the greatest security risk. What is this? ")
responses = ["Administrator", "Admin", "admin", "administrator", "Administrators", "administrators", "root", "Root"]

if question6 in responses:
    print("Correct! Excellent work.")

    print("Thank you for your hard work in the field. We'll be in touch with your next mission soon.")

    print("In the meantime, enjoy a flag!")

    print("corctf{alw4y5_l3m0n_7h1nk_b3f0r3_y0u_c0mm1t_cr1m3}")
else:
    print("Incorrect. Please try again next time!") 
    exit()
