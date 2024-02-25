import csv
import sys 

def main():
    list = return_csv_file()

def return_csv_file():
    with open("data/originalfile.csv") as csvf:
        file = csv.reader(csvf,delimiter=',')
        list = []
        for data in file: 
            list.append(
                (data[0],float(data[1]),float(data[2]))
            )
        return list
    
main()

