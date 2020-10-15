import math

ret = [2, 3, 5, 7, 11, 13]

while len(ret) < 10001:
    test = ret[-1] + 1
    found = False

    print(len(ret))
    while not found:
        max_i = math.floor(math.sqrt(test))
     
        for i in range(max_i, 1, -1):
            if test % i == 0:
                break
            if i == 2:
                ret.append(test)
                found = True  
                
        test += 1

print(ret[-1])