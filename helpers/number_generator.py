import random
import sys


rows = sys.argv[2]
columns = sys.argv[3]
range = sys.argv[4]
filename = sys.argv[5]
file = open(filename,'w')

if sys.argv[1] == 1:
    for row in rows:
        for col in columns:
            file.write(str(random.uniform(0,range)) + " ")
        file.write("\n")
else:
    for row in columns:
        file.write(str(random.uniform(0,range)) + "\n")