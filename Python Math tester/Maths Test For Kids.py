#Module Title: Programming Strand | Module Code: COMP10082
#Name: Dayeeta Das | NTU ID: N0830182 
#This is a Maths test for kids with timing and scoring.
#A function  named instructions is created to store all the instructions for the exam
def instructions():
    print("""
           This is a Maths Test with 3 different levels:
           1)easy
           2)medium
           3)hard
           Each level comprises of 20 questions.
           Calculators are allowed.
           The total time of the exam is 2 mins.
           The questions and answers of this test
           along with the name of the candidate and the level will be stored
           in a file.
           """)
import random
import time
#The current time is saved
currTime = time.ctime()
#the starting time of the exam is initialized
startTime=time.time()
level=""
n=0
r=0
score=0
#The numbers used for forming the equations in the different levels are stored in different lists
e=[2,4,6,8]
m=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
h=[11,12,13,14,15,16,17,18,19]
#The operators are stored in a list
operators=["+", "-", "*", "/"]
#The levels and the numbers to be used for making the equations are stored in a dictionary
levels={"easy":e, "medium":m, "hard":h}
question=""
#The function instruction gets called
instructions()
#A file is opened to write down the details of the student along with the questions and answers
file=open("name.txt","a")
#The names of the students getting the higher grades are stored in this file
scores=open("high scores.txt","a")
name=input("Enter your name here:")
#checks if the name is valid or not
while not name.isalpha():
    print("Invalid input")
    name=input("Enter your name here:")
file.write(name)
file.write("\n")
while True:
    level=input("Enter which level you want to start with here:")
    if level in levels:
        break
    else:
        print("Level does not exist")
        continue
file.write("level:")
file.write(level)
file.write("\n")
print("The starting time of your exam is:",currTime)
while n<20:
    r=levels[level]
    #Each time random numbers will be generated to create different set of equations
    num1=random.choice(r)
    num2=random.choice(r)
    #Ending time is set to 2 minutes
    endTime=startTime+120
    #The operators will be chosen by the computer at random
    op=random.choice(operators)
    #the question is stored
    q=float(eval(str(num1)+op+str(num2)))
    question="Q:"+str(num1)+op+str(num2)+"="
    print(question)
    file.write(question)
    file.write("\n")
    file.write("A:")
    file.write(str(q))
    file.write("\n")
    #the answer is taken as input
    a=float(input("A:"))
    if q==a:
        print("Correct!")
        #if the answer is right 2 points are awarded
        score+=2
    else:
        print("Wrong!")
        #if the answer is wrong 2 points is deducted and the correct answer is shown
        score-=2
        print("The answer is:",q)
    n+=1
    #operation performed if the exam finishes on time
    if n==20 and time.time()>endTime:
        print("Your total score is:",score)
        print("You completed just in time!")
        break
    #operation performed if the exam finishes before given time
    elif n==20 and time.time()<endTime:
        print("Your total score is:",score)
        print("You completed before time!")
        break
    #operation performed if the exam does not finish on time
    elif n!=20 and time.time()>endTime:
        print("Your total score is:",score)
        print("You were unable to complete the entire test!")
        break
if score>20:
    scores.write(name)
#The scores file gets closed
scores.close()
#the text file gets closed
file.close()
print("\n")
print("\n")
#the answersheet is displayed after the exam gets over
file=open("name.txt","r")
print("Here's the answer sheet:")
answersheet=file.read()
print(answersheet)
input("Press the enter key to exit:")
        

    
