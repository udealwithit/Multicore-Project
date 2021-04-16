import random
import sys


rows = int(sys.argv[2])
columns = int(sys.argv[3])
maxNum = int(sys.argv[4])
filename = sys.argv[5]
file = open(filename,'w')
print(sys.argv)
if sys.argv[1] == '1':
    for row in range(rows):
        for col in range(columns):
            file.write(str(random.uniform(0,maxNum)) + " ")
        file.write("\n")
else:
    for row in range(columns):
        file.write(str(random.uniform(0,maxNum)) + "\n")
file.close()