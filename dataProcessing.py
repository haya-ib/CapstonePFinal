#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inline
import matplotlib
import pandas as pd
from sklearn import naive_bayes, tree, svm  , metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np


#https://towardsdatascience.com/demystifying-confusion-matrix-confusion-9e82201592fd
# import csv
# reading the csv file which is the training set will be test with our dataset
kaggleData = pd.read_csv('trainfileorignal.csv')
kaggleData.dropna(inplace=True) #remove any missing value
kaggleData["text"] = kaggleData["Comment"].str.split(",", n=1, expand=True) #pick the column of dataset
trainset = pd.DataFrame() # asign a panda datafram of training set
trainset['text'] = kaggleData["text"]
trainset['label'] = kaggleData["Insult"]
shuffleData = shuffle(trainset) # make shuffle of the training set
tfIDf_w = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=3, stop_words='english', use_idf=True,
                             token_pattern=u"\w{4,}", lowercase=True)
# training the text from reading the file
x = tfIDf_w.fit_transform(shuffleData['text'])
# training the label from reading file
y = shuffleData['label']
# siplitting dataset to train and test/ validation set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

# DT Model:
DT = tree.DecisionTreeClassifier()
DT.fit(x, y)

# NB model:
NBClasssifier = naive_bayes.MultinomialNB()
NBClasssifier.fit(x_train, y_train)

# SVM Model:
SVM = svm.SVC(gamma='scale')
SVM.fit(x, y)

def naiveBayersClassification(text):
    doc = tfIDf_w.transform([text])
    return NBClasssifier.predict(doc)[0]

def DecsionTree(text):
    # DT = tree.DecisionTreeClassifier()
    # DT.fit(x, y)
    doc = tfIDf_w.transform([text])
    return DT.predict(doc)[0]


def SVM(text):
    doc = tfIDf_w.transform([text])
    return DT.predict(doc)[0]


def infoOfClassification():
    confusion = confusion_matrix(y_test, DT.predict(x_test))
    reprt = classification_report(y_test, DT.predict(x_test))
    accuracy = accuracy_score(y_test, DT.predict(x_test)) * 100

    #http://www.tarekatwan.com/index.php/2017/12/how-to-plot-a-confusion-matrix-in-python/
    #http: // www.tarekatwan.com / index.php / 2017 / 12 / how - to - plot - a - confusion - matrix - in -python /
    #plt.clf()
    #plt.imshow(confusion, interpolation='nearest', cmap=plt.cm.twilight)
    #classNames = ['Negative', 'Positive']
    #plt.title('Before DT Classification - Confusion Matrix \nAccuracy:{0:.3f}'.format(accuracy))
    #plt.ylabel('True label')
    #plt.xlabel('Predicted label')
    #tick_marks = np.arange(len(classNames))
    #plt.xticks(tick_marks, classNames, rotation=45)
    #plt.yticks(tick_marks, classNames)
    #s = [['TN', 'FP'], ['FN', 'TP']]
    #for i in range(2):
    #    for j in range(2):
    #         plt.text(j, i, str(s[i][j]) + " = " + str(confusion[i][j]))

    #plt.savefig('static/images/Before_Prediceted.png')
    #plt.show()

    return confusion, reprt, accuracy

infoOfClassification()

