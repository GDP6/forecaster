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
    
with open("s2features", "wb") as f:
    pickle.dump(feature, f, pickle.HIGHEST_PROTOCOL)
