import csv

MAX_COUNT = 1000
writeFile = open('top-' + str(MAX_COUNT) + '.csv', 'wb')
writer = csv.writer(writeFile)
data = []
with open('top-1m.csv') as readFile:  
    reader = csv.reader(readFile)
    count = 0
    for row in reader:
        data.append(row)
        count += 1
        if count == 1000:
        	break

writer.writerows(data)
