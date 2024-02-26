# receive arguments from the command line

import sys
import shutil
import time
print("Running ", sys.argv[0])
# print the number of arguments
print(len(sys.argv))

# print the arguments
for arg in sys.argv:
    print(arg)

i = 0
file = open("payload1.txt", "a")
while i<10:
    print("Payload1: Running ", sys.argv[0], " iteration ", i)
    i += 1
    time.sleep(2)
    file.write("Payload1: Running " + sys.argv[0] + " iteration " + str(i) + "\n")

file.close()

print("Payload1: Done writing to file")

# move file to the data folder

shutil.move("payload1.txt", "data/payload1.txt")

while True:
    time.sleep(2)
    print("Payload1: Running ", sys.argv[0], " iteration ", i)
    i += 1