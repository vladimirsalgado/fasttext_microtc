#
#this code is to cut a file in a validation and train part
#arguments: genvaltra.py inputfile percenttrainpart

#import os
import subprocess
import sys
import re


inputfile = sys.argv[1]
#percenttrain = sys.argv[2]


print("COMMAND TO EXECUTE: wc " + inputfile)

p = subprocess.Popen("wc " + inputfile, shell=True)

p.wait()

output = p.stdout.read().decode()

print(output)

capture = re.split('\n|\t',output)

print(capture)


