import math

number = 600851475143
ret = []
i = 2

while number != 1:
    if number % i == 0:
        number /= i
        ret.append(i)
    else:
        i += 1

print(ret[-1])

    
