for a in range(1001):
    for b in range(1001):
        for c in range(1001):
            if a + b + c == 1000 and a * a + b * b == c * c and a < b and b < c:
                print(a * b * c)

