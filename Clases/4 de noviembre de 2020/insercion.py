fechanum = [(1, 1), (3, 3), (4, 2), (6, 4), (8, 5), (11, 7), (17, 6), (18, 8)]
for i in range(1,len(fechanum)):
    for j in range(0,i):
        if fechanum[i][1] < fechanum[j][1]:
            fechanum[i],fechanum[j]=fechanum[j],fechanum[i]
            #fechanum.insert(j,fechanum[j][1])
            #fechanum.pop(j+1)
