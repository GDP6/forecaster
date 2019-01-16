import csv
import pickle
time = []
sensor2 = []
sensor2diff = []

with open('rateData.csv', 'rt') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        time.append(float(row[0]))
        sensor2.append(float(row[3]))
        sensor2diff.append(float(row[4]))
        
feature = [0] * len(sensor2diff)

i = 0
while i < len(sensor2diff):
    if(sensor2diff[i] < -0.3):
        startIndex = i
        endIndex = i
        for p in range(i,i + 100):
            if(sensor2diff[p] < -0.3):
                endIndex = p
            else:
                i = endIndex
                break
        i = endIndex
        if(startIndex != endIndex):
            tempDropped = sensor2[endIndex] - sensor2[startIndex]
            if(tempDropped < -5):
                for i in range(startIndex, endIndex):
                        feature[i] = 1
               
    i += 1
i = 0
while i < len(sensor2diff):
    if(sensor2diff[i] < -0.0):
        startIndex = i
        endIndex = i
        for p in range(i,i + 100):
            if(sensor2diff[p] < -0.05):
                endIndex = p
            else:
                i = endIndex
                break
        i = endIndex
        if(startIndex != endIndex):
            tempDropped = sensor2[endIndex] - sensor2[startIndex]
            if((tempDropped < -1.0) & (tempDropped > -5.0)):
                for i in range(startIndex, endIndex):
                        feature[i] = 2
    i += 1
    
i = 0
while i < len(sensor2diff) - 100:
    if(sensor2diff[i] > -0.0):
        startIndex = i
        endIndex = i
        for p in range(i,i + 100):
            if(sensor2diff[p] > 0.05):
                endIndex = p
            else:
                i = endIndex
                break
        i = endIndex
        if(startIndex != endIndex):
            tempDropped = sensor2[endIndex] - sensor2[startIndex]
            if(tempDropped > 5.0):
                for i in range(startIndex, endIndex):
                        feature[i] = 3
    i += 1
    
for g in range(len(time) - 60):
    if(time[g] < time[g - 1]):
        for a in range(g,g + 60):
            feature[a] = 5
    elif(time[g] > time[g -1] + 300):
        for a in range(g,g + 60):
            feature[a] = 5
    elif((time[g] > float(1514590000)) & (time[g] < float(1514710000))):
        feature[g] = 5
    
#print(feature)

with open("s2features", "wb") as f:
    pickle.dump(feature, f, pickle.HIGHEST_PROTOCOL)
    
    
tempvsLength = []
TempLossPerSec3 = []
TempLossPerSec1 = []
look1start = True
look1end = False
look3start = False
look3end = False
start1 = 0
start3 = 0
end1 = 0
end3 = 0
for i in range(len(feature)):
    if(look1start):
        if(feature[i] == 1):
            start1 = i
            look1start = False
            look1end = True
    elif(look1end):
        if(feature[i] != 1):
            end1 = i
            look1end = False
            look3start = True
    elif(look3start):
        if(feature[i] == 3):
            start3 = i
            look3start = False
            look3end = True
    elif(look3end):
        if(feature[i] != 3):
            end3 = i
            look3end = False
            look1start = True
            tempvsLength.append([sensor2[start3],end3 - start3])
            TempLossPerSec3.append((sensor2[end3] - sensor2[start3]) / (time[end3] - time[start3]))
            TempLossPerSec1.append((sensor2[end1] - sensor2[start1]) / (time[end1] - time[start1]))

            
import numpy as np

print(np.mean(TempLossPerSec1))
print(np.mean(TempLossPerSec3))

print(np.polyfit(np.column_stack(tempvsLength)[0],np.column_stack(tempvsLength)[1],1))

#0.00857402379537
#[ -1.29644032  72.14327532]

        
        
