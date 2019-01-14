import pickle
import csv

       
time = []
sensor3 = []
with open("specifity", "rb") as f:
    specifity = pickle.load(f)
    
with open("percision", "rb") as f:
    percision = pickle.load(f)
    
with open("negativePercision", "rb") as f:
    negativePercision = pickle.load(f)
    
with open("sensitivty", "rb") as f:
    sensitivty = pickle.load(f)

with open("s2features", "rb") as f:
    feature = pickle.load(f)
    
with open('rateData.csv', 'rt') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        time.append(float(row[0]))
        sensor3.append(float(row[2]))
        


def getPercision(length, tempDiffSec):
    b = int(tempDiffSec * -4000)
    if(b < 0):
        b = 0
    return percision[length][b]

def getSpecifity(length, tempDiffSec):
    b = int(tempDiffSec * -4000)
    if(b < 0):
        b = 0
    return specifity[length][b]

def getSensitivty(length, tempDiffSec):
    b = int(tempDiffSec * -4000)
    if(b < 0):
        b = 0
    return sensitivty[length][b]

def getThreshold(sensitivty,specifity):
    a = 1
    b = 1
    return (sensitivty*a) + (specifity*b)

sensor3log = []
sensor3feature = []
sensor3time = []

def recieveSensor(temp,t):
    sensor3log.append(temp)
    sensor3time.append(t)
    if(len(sensor3log) > 25):
        g = len(sensor3log)-1
        highestSpecifity = 0
        highestLength = 5
        highestTempDiffSec = 0
        for length in range(5,20):
            timePassed = sensor3time[g] - sensor3time[g - length]
            tempDiff = sensor3log[g] - sensor3log[g - length]
            tempDiffSec = tempDiff / timePassed
            cSpecifity = getSpecifity(length-5,tempDiffSec)
            if(cSpecifity > highestSpecifity):
                highestSpecifity = cSpecifity
                highestLength = length
                highestTempDiffSec = tempDiffSec
        if(highestSpecifity > 0.99):
            sensor3feature.append(1)
            for c in range(g - highestLength,g):
                sensor3feature[c] = 1
        else:
            sensor3feature.append(0)
    else:
        sensor3feature.append(5)
        
        
        
for g in range(len(sensor3)):
    recieveSensor(sensor3[g],time[g])


    
    

    
    


    
    

