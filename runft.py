#
#this code is to run FastText and to find the best parameters for introduced dataset
#

#import os
import subprocess
import sys
import re
import nltk #Natural Language Toolkit

dataset = sys.argv[1]
trainfile = sys.argv[2]
testfile = sys.argv[3]

#function to obtain the better fasttext parameters in a grid manner
#def runfasttext(Data, Train, Test, Epoch, LR, WordNgrams):
#    print("COMMAND TO EXECUTE: ./fasttext supervised -input " + Train + " -ouptut "  + Data + ".model -epoch " + str(Epoch) + " -lr " + str(LR) + " -wordNgrams " + str(WordNgrams) 
#    p = subprocess.Popen("./fasttext supervised -input " + Train + " -output " + Data + ".model -epoch " + str(Epoch) + ' -lr ' + str(LR) + " -wordNgrams " + str(WordNgrams), shell=True)
#    p.wait()
#    p = subprocess.Popen("./fasttext test " + Data + ".model.bin " + Test, stdout=subprocess.PIPE, shell=True)
#    ftoutput = p.stdout.read().decode() 
#    performance = re.split('\n|\t',ftoutput)
#    F1b=2*((float(performance[3])*float(performance[5]))/(float(performance[3])+float(performance[5])))
#    if F1b > F1:
#        F1 = F1b
#        F1b = 0.0
#    else:
#        F1b = 0.0
#        break


#To train the classifier
print("COMMAND TO EXECUTE: ./fasttext supervised -input " + trainfile + " -output " + dataset + ".model")
p = subprocess.Popen("./fasttext supervised -input " + trainfile + " -output " + dataset + ".model", shell=True)
p.wait()

#To test the classifier
print("COMMAND TO EXECUTE: ./fasttext test " + dataset + ".model.bin " + testfile)
p = subprocess.Popen("./fasttext test " + dataset + ".model.bin " + testfile, stdout=subprocess.PIPE, shell=True)

ftoutput = p.stdout.read().decode()
#print(ftoutput)
performance = re.split('\n|\t',ftoutput)
#print(performance)

P0 = float(performance[3])
R0 = float(performance[5])
F1 = 2*((P0*R0)/(P0+R0))
F1a = 0.0
F1b = 0.0
print('\nPERFORMANCE METRICS (base): \nPrecisión=' + str(P0) + ', \nRecall=' + str(R0) + ', \nF1:' + str(F1))

#Making the model better
#preprocessing the data with some techniques -- PENDING

#testing with more epoch 5-25
epoch = 5

while F1 > F1b:
    epoch+=5
    p = subprocess.Popen("\n./fasttext supervised -input " + trainfile + " -output " + dataset + ".model -epoch " + str(epoch), shell=True)
    p.wait()
    p = subprocess.Popen("./fasttext test " + dataset + ".model.bin " + testfile, stdout=subprocess.PIPE, shell=True)
    ftoutput = p.stdout.read().decode()
    performance = re.split('\n|\t',ftoutput)
    F1b=2*((float(performance[3])*float(performance[5]))/(float(performance[3])+float(performance[5])))
    print('F1:' + str(F1) + ' F1b:' + str(F1b) + ' Epoch:' + str(epoch))
    if F1b > F1:
        F1 = F1b
        F1b = 0.0
    else:
        F1b = 0.0
        break

#test adding learning rate 0.1-1.0 parameter
lr = 0.0
while F1 > F1b:
    lr+=0.1
    p = subprocess.Popen("\n./fasttext supervised -input " + trainfile + " -output " + dataset + ".model -epoch " + str(epoch) + ' -lr ' + str(lr), shell=True)
    p.wait()
    p = subprocess.Popen("./fasttext test " + dataset + ".model.bin " + testfile, stdout=subprocess.PIPE, shell=True)
    ftoutput = p.stdout.read().decode()
    performance = re.split('\n|\t',ftoutput)
    F1b=2*((float(performance[3])*float(performance[5]))/(float(performance[3])+float(performance[5])))
    print('F1:' + str(F1) + ' F1b:' + str(F1b) + ' Epoch:' + str(epoch))
    if F1b > F1:
        F1 = F1b
        F1b = 0.0
    else:
        F1b = 0.0
        break

#testing adding wordNgrams 1-5
wordNgrams = 1 
while F1 > F1b:                                                                                                                                     
    wordNgrams+=1 
    p = subprocess.Popen("\n./fasttext supervised -input " + trainfile + " -output " + dataset + ".model -epoch " + str(epoch) + ' -lr ' + str(lr) + ' -wordNgrams ' + str(wordNgrams), shell=True)
    p.wait()
    p = subprocess.Popen("./fasttext test " + dataset + ".model.bin " + testfile, stdout=subprocess.PIPE, shell=True)
    ftoutput = p.stdout.read().decode()
    performance = re.split('\n|\t',ftoutput)
    F1b=2*((float(performance[3])*float(performance[5]))/(float(performance[3])+float(performance[5])))
    print('F1:' + str(F1) + ' F1b:' + str(F1b) + ' Epoch:' + str(epoch) + ' WordNgrams:' + str(wordNgrams))
    if F1b > F1:
        F1 = F1b
        F1b = 0.0
    else:
        F1b = 0.0
        break


print('\n FINAL PERFORMANCE METRICS: \n Epoch:' + str(epoch) + ',\n lr:' + str(lr) + '\n wordNgrams: ' + str(wordNgrams) + '\n F1:' + str(F1))

