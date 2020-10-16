one = 1
two = 2
ret = 0

while one <= 4000000 or two <= 4000000:
    if one % 2 == 0 and one <= 4000000:
        ret += one
    if two % 2 == 0 and two <= 4000000:
        ret += two

    one += two
    two += one

print(ret)
