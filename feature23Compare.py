ftp = 0
ftn = 0
ffp = 0
ffn = 0

def positiveFuzz(h):
    for a in range(h - 5,h +5):
        if(feature[a] == 1):
            return True
    return False

def negativeFuzz(h):
    for a in range(h - 5,h +5):
        if(sensor3feature[a] == 1):
            return True
    return False

for h in range(len(sensor3feature)-5):
    feature3 = sensor3feature[h]
    feature2 = feature[h]
    if(feature3 == 1 and positiveFuzz(h)):
        ftp += 1
    elif(feature3 == 0 and feature2 == 0):
        ftn += 1
    elif(feature3 == 1 and feature2 == 0):
        ffp += 1
    elif(feature3 == 0 and feature2 == 1):
        ffn += 1
        
        
print(ftp)
print(ftn)
print(ffp)
print(ffn)

fSensitivity = ftp/(ftp+ffn)
fSpecifity = ftn/(ftn+ffp)
fPercision = ftp/(ftp+ffp)
fNegPercision = ftn/(ftn + ffn)
fAccuracy = (ftp + ftn) / (ftp + ftn + ffn + ffp)

print(fSensitivity)
print(fSpecifity)
print(fPercision)
print(fNegPercision)
print(fAccuracy)
        
