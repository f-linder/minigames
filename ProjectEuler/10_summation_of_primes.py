import math

# THIS TAKES TOO LONG

def check_prime(n):
    check = n
    for i in range(2, check):
        if n % i == 0:
            return False
        check = n / i
    else:
        return True

list = []

for potential_prime in range(1, 2000000):
    if check_prime(potential_prime):
        list.append(potential_prime)
        print(potential_prime)

print(sum(list))


