import pickle
import csv
time = []
sensor3 = []

with open('rateData.csv', 'rt') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        time.append(float(row[0]))
        sensor3.append(float(row[2]))
        
with open("s2features", "rb") as f:
    feature = pickle.load(f)

tp = [[0 for i in range(40)] for j in range(20)]
tn = [[0 for i in range(40)] for j in range(20)]
fp = [[0 for i in range(40)] for j in range(20)]
fn = [[0 for i in range(40)] for j in range(20)]



for a in range(5,25):
    print(a) 
    for b in range(40):
        for g in range(25,len(sensor3) - 5):
            timePassed = time[g] - time[g - a]
            tempDiff = sensor3[g] - sensor3[g - a]
            tempDiffSec = tempDiff / timePassed
            if(tempDiffSec < float(-(b)/4000)):
                if(feature[g] == 1 or feature[g - 5] == 1 or feature[g + 5] == 1):
                    tp[a - 5][b] += 1
                elif(feature[g] != 1):
                    fp[a - 5][b] += 1
            else:
                if(feature[g] == 1):
                    fn[a - 5][b] += 1
                elif(feature[g] != 1):
                    tn[a - 5][b] += 1
                    
sensitivty = [[0 for i in range(40)] for j in range(20)]
specifity = [[0 for i in range(40)] for j in range(20)]
percision = [[0 for i in range(40)] for j in range(20)]
negativePercision = [[0 for i in range(40)] for j in range(20)]
accuracy = [[0 for i in range(40)] for j in range(20)]

for a in range(20):
    for b in range(40):
        try:
            sensitivty[a][b] = tp[a][b] / (tp[a][b] + fn[a][b])
        except ZeroDivisionError:
             sensitivty[a][b] = sensitivty[a][b-1]
        try:
            specifity[a][b] = tn[a][b] / (tn[a][b] + fp[a][b])
        except ZeroDivisionError:
            specifity[a][b] = specifity[a][b-1]
        try:
            percision[a][b] = tp[a][b] / (tp[a][b] + fp[a][b])
        except ZeroDivisionError:
            percision[a][b] = percision[a][b-1]
        try:
            negativePercision[a][b] = tn[a][b] / (tn[a][b] + fn[a][b])
        except ZeroDivisionError:
            negativePercision[a][b] = negativePercision[a][b-1]
        try:
            accuracy[a][b] = (tp[a][b] + tn[a][b]) / (tp[a][b] + fp[a][b] + tn[a][b] + fn[a][b])
        except ZeroDivisionError:
            accuracy[a][b] = accuracy[a][b-1]


print(tp)
print(tn)
print(fp)
print(fn)



with open("percision", "wb") as f:
    pickle.dump(percision, f, pickle.HIGHEST_PROTOCOL)

with open("specifity", "wb") as f:
    pickle.dump(specifity, f, pickle.HIGHEST_PROTOCOL)
with open("sensitivty", "wb") as f:
    pickle.dump(sensitivty, f, pickle.HIGHEST_PROTOCOL)
with open("negativePercision", "wb") as f:
    pickle.dump(negativePercision, f, pickle.HIGHEST_PROTOCOL)
with open("accuracy", "wb") as f:
    pickle.dump(accuracy, f, pickle.HIGHEST_PROTOCOL)

