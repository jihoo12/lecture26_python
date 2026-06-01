import random
max = 50
try_count = 7
number = random.randint(0,max)
iswin = False
for i in range(try_count):
    n =  int(input())
    if n > number:
        print("down")
    elif n < number:
        print("up")
    elif n == number:
        print("you win")
        iswin = True
        break

if iswin == False:
    print("you lose")
