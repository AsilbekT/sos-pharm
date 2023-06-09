import csv
with open('/Users/asilbekturgunboev/Desktop/pharmacy/test.csv', 'r',) as file:
    reader = csv.reader(file, delimiter = '\t')
    for row in reader:
        print(len(row))