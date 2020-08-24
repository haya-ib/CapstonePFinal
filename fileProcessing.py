import dataProcessing
import pandas as pd
import csv
import numpy as np
from matplotlib import style
from matplotlib import pyplot as plt

# when file uploaded will read and write the information from the file to the row with new prediction of row2 which is the
#text for the new lable

def readingAndPredicting(csv_input):
    prediction = []
    counter = 0
    for row in csv_input:
        if counter == 0:
            Arow = []
            Arow.append(row[0])
            Arow.append(row[1])
            Arow.append(row[2])
            Arow.append(row[3])
            Arow.append(row[4])
            Arow.append("newlabel")
            prediction.append(Arow)
            counter = counter + 1
        else:
            Arow = []
            Arow.append(row[0])
            Arow.append(row[1])
            Arow.append(row[2])
            Arow.append(row[3])
            Arow.append(row[4])
            #new label will be predict with DT classifier in the row[2] where the 'text' is.
            Arow.append(str(predict(row[2])))
            prediction.append(Arow)
            counter = counter + 1
    with open('newPrediction.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(prediction)
    return prediction

def predict(text):
    return dataProcessing.DecsionTree(text)

