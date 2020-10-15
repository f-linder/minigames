num = 0
found = False

while not found:
    num += 20

    for i in range(20, 10, -1):
        if num % i != 0:
            break
        if i == 11:
            found = True

print(num)