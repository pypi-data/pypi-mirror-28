from random import randint

count0 = 0
count1 = 0

for i in range(0, 10000000):
    if randint(0, 1) == 0:
        count0 += 1
    else:
        count1 += 1

print("0: ", count0)
print("1: ", count1)
