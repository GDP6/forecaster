import pickle
import csv
from math import fmod
       
time = []
sensor3 = []
sensor2 = []
with open("specifity", "rb") as f:
    specifity = pickle.load(f)
    

with open("s2features", "rb") as f:
    feature = pickle.load(f)
    
with open('rateData.csv', 'rt') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        time.append(float(row[0]))
        sensor3.append(float(row[2]))
        sensor2.append(float(row[3]))
        


def getSpecifity(length, tempDiffSec):
    b = int(tempDiffSec * -4000)
    if(b < 0):
        b = 0
    return specifity[length][b]



def checkForFeature5(timelog):
    g = len(sensor3log)-1
    if(len(timelog) < 30):
        return True
    for timeback in range(30):
        if(timelog[g - timeback] < timelog[g-timeback - 1]):
            return True
        elif(timelog[g - timeback] > timelog[g - timeback - 1] + 300):
            return True
    return False
            
    

def checkForFeature1(sensor3log,timelog):
    g = len(sensor3log)-1
    highestSpecifity = 0
    highestLength = 5
    highestTempDiffSec = 0
    for length in range(5,20):
        timePassed = timelog[g] - timelog[g - length]
        tempDiff = sensor3log[g] - sensor3log[g - length]
        tempDiffSec = tempDiff / timePassed
        cSpecifity = getSpecifity(length-5,tempDiffSec)
        if(cSpecifity > highestSpecifity):
            highestSpecifity = cSpecifity
            highestLength = length
            highestTempDiffSec = tempDiffSec
    if(highestSpecifity > 0.99):
        return [True,highestLength]
    else:
        return [False,0]

def lengthOfFeature3(currentTemp):
    return int(72.14327532 - (1.29644032*currentTemp))

def feature3TempIncrease(timePassed):
    return (timePassed * 0.00857402379537)

def feature1TempDecrease(timePassed):
    return (timePassed * -0.0259821576177)


def lengthOfFeature0Heat(currentTemp):
    return 773.8850914210703 - (currentTemp * 5.209158376824304)

def lengthOfFeature0Cold(currentTemp):
    return 667.9497021485934 + (currentTemp * 52.93806785791462)

def heatingIncrease(currentTemp):
    return 11 - (currentTemp * 0.16)
    
def coldingDecrease(currentTemp):
    return 4.61 - (currentTemp  * 0.117)

def heatingRatio(firstTime, lastTime, currentTime, heatingTime, coldingTime):
    currentPhase = fmod(currentTime - firstTime,heatingTime + coldingTime)
    lastPhase = fmod(lastTime - firstTime,heatingTime + coldingTime)
    if(currentPhase > heatingTime and lastPhase < heatingTime):
        timeHeating =  heatingTime - lastPhase;
    elif(currentPhase > heatingTime and lastPhase > heatingTime):
        timeHeating = 0.0;
    elif(currentPhase < heatingTime and lastPhase < heatingTime):
        timeHeating = currentPhase - lastPhase;
    elif(currentPhase < heatingTime and lastPhase > heatingTime):
        timeHeating = currentPhase;
    ratio = (timeHeating)/(currentTime-lastTime)
    return ratio

def feature0TempChange(currentTemp, currentTime, firstTime, lastTime):
    gainPerSecond = heatingIncrease(currentTemp) / lengthOfFeature0Heat(currentTemp)
    print(currentTemp)
    lossPerSecond = coldingDecrease(currentTemp) / lengthOfFeature0Cold(currentTemp)
    heatRatio = heatingRatio(firstTime, lastTime, currentTime, lengthOfFeature0Heat(currentTemp), lengthOfFeature0Cold(currentTemp));	
    gainThisTick = gainPerSecond*heatRatio * (currentTime-lastTime);
    lossThisTick = lossPerSecond*(1-heatRatio) * (currentTime-lastTime);
    tempChange = (gainThisTick + lossThisTick)
    print(tempChange)
    return tempChange
     
sensor3log = []
sensor3feature = []
sensor2EstimateTemp = []
timelog = []
lastFeature1 = False
feature3left = 0
currentTemp = 50
f0startTime = 0

def recieveSensor(temp,t):

    global lastFeature1
    global feature3left
    global currentTemp
    global f0CycleStart
    global f0startTime
    
    sensor3log.append(temp)
    timelog.append(t)
    g = len(sensor3log)-1
    
    if(timelog[g] - f0startTime > 10000):
        f0startTime = timelog[g]
    if(feature3left >= 0):
        sensor3feature.append(3)
        currentTemp += feature3TempIncrease(timelog[g] - timelog[g-1])
        feature3left -= 1;
    elif(checkForFeature5(timelog)):
        sensor3feature.append(5)
    else:
        checkF1 = checkForFeature1(sensor3log,timelog)
        if(checkF1[0]):
            lastFeature1 = True
            sensor3feature.append(1)
            f0tof1 = 0
            for length in range(checkF1[1]):
                if(sensor3feature[g - length] != 1):
                    sensor3feature[g-length] = 1
                    f0tof1 += 1
            currentTemp += feature1TempDecrease(timelog[g] - timelog[g - f0tof1 - 1])
        elif(lastFeature1 == True):
            lastFeature1 = False
            feature3left = lengthOfFeature3(currentTemp)
            currentTemp += feature0TempChange(currentTemp, timelog[g], f0startTime, timelog[g-1]) 
            sensor3feature.append(0)
        elif(lastFeature1 == False):
            sensor3feature.append(0)
            currentTemp += feature0TempChange(currentTemp, timelog[g], f0startTime, timelog[g-1]) 

            
    if(currentTemp > 59):
        currentTemp = 59
    elif(currentTemp < 35):
        currentTemp = 35
    sensor2EstimateTemp.append(currentTemp)
    
    
    
    
    
startnum = 23000
num = 28500

for g in range(startnum,num):
    recieveSensor(sensor3[g],time[g])

#print(feature[startnum:num])
#print(sensor3feature)

import matplotlib.pyplot as plt
plt.plot(timelog[0:num],sensor2EstimateTemp[0:num],"")
plt.plot(timelog[0:num],sensor2[startnum:num],"")                    
plt.show()

    


    
    

