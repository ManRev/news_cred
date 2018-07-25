import numpy as np
import re
import matplotlib.pyplot as plt
import csv
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from urllib.parse import urlparse
from wrap_up import string_process as sp
import pandas as pd

stopword = set(stopwords.words('english'))
bool = 'of' in stopword
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

import ast
def open_all_com(path, c=0):
    f = open(path, 'r')
    dict_list = []
    for line in f.readlines():
        line = line.strip()
        name = line.split("<<||>>")
        #print(name)
        row = line.split('"')
        if len(row) == 3:
            last = ast.literal_eval(row[1])
            last = last[0]
            two = row[0].split(',')
            #print(len(two))
            if two[5] != "Current Domain":
                #print(len(name))
                c += 1
                dict_list.append(two)
    headers_test = ['number','publisher', 'visited_url', 'timestamp', 'destination_url', 'destination_domain', 'headline',
                    'CRN', 'widget_type', 'prob']
    dict_tot = pd.DataFrame(dict_list, columns=headers_test)
    return dict_tot

def word_diet(dict_tot, testData):
    spam = 0
    tot = 0
    tot_test = 0
    for index, row in dict_tot.iterrows():
            tot+=1
            head = row['headline']
            if len(testData[testData['raw'] == head]) != 0:
                tot_test += 1
                ind = testData[testData['raw'] == head].index.values.astype(int)[0]
                df = testData.ix[ind]
                if int(df['label']) == 1:
                    spam+=1
    print("All Data Set: ")
    print("Spam: " + str(spam))
    print("Total= " + str(tot))
    print("Total= " + str(tot_test))
    print("------------------------")


def publishers_diet(dict_tot, testData, target, name):
    tot_mat = []
    for publisher in target :
        spam = 0
        tot = 0
        tot_test = 0
        for index, row in dict_tot.iterrows():
            if row['publisher'] == publisher:
                tot+=1
                head = row['headline']
                #print(testData[testData['raw'] == head])
                #print(head)
                if len(testData[testData['raw'] == head]) != 0:
                    tot_test += 1
                    ind = testData[testData['raw'] == head].index.values.astype(int)[0]
                    df = testData.ix[ind]
                    if int(df['label']) == 1:
                        spam+=1
        tot_mat.append([publisher, spam, tot, tot_test])
        #print("Publisher: " + str(publisher))
        #print("Spam: " + str(spam))
        #print("Total= " + str(tot))
        #print("Total= " + str(tot_test))
        #print("------------------------")
    #tot = np.asarray(tot)
    with open(name, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=",")
        wr.writerow(tot_mat)
