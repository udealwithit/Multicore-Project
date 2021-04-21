import random
import sys


rows = int(sys.argv[2])
columns = int(sys.argv[3])
maxNum = int(sys.argv[4])
filename = sys.argv[5]
file = open(filename,'w')
if sys.argv[1] == '1':
    for row in range(rows):
        for col in range(columns):
            file.write(str(random.uniform(0,maxNum)) + " ")
        file.write("\n")
elif sys.argv[1] == '0':
    for row in range(columns):
        file.write(str(random.uniform(0,maxNum)) + "\n")
else:
    for row in range(rows):
        file.write(str(random.randint(0, maxNum)) + " ")
file.close()