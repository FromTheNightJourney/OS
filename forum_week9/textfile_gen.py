import random

random_numbers = [random.randint(1, 1000) for _ in range(1000)]

with open("nums.txt", "w") as file:
    for number in random_numbers:
        file.write(str(number) + "\n")
