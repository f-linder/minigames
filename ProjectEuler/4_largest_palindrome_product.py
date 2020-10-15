
ret = []

for i in range(999, 99, -1):
    for j in range(999, 99, -1):
        string = str(i * j)
        if string == string[::-1]:
            ret.append(int(string))
            finished = True
          
ret.sort()
print(ret[-1])


