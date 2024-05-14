import random

maxRange = 1000
minRandom = 0
maxRandom = 4999

with open("nums.txt", "w") as file:
    for _ in range(maxRange):
        file.write(str(random.randint(minRandom, maxRandom)) + "\n")