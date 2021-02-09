#write a python program that asks a user to guess an integer between 1 and 15!
import random
random_num = random.randint(1,15) #generates a random int between 0 and 15
guess = None #generate an empty variable
count = 0
while guess != random_num:
    count+=1
    guess = int(input('Take a guess: '))
    if guess == random_num:
        print('Congratulations, you guessed my number in', count, 'trials!')
        break #exit the loop and end the program if it is correctly guessed
    elif guess<random_num:
        print('Your guess is too low.')
    else:
        print('Your guess is too high.')
