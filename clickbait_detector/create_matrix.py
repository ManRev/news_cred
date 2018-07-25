import csv
import matplotlib.pyplot as plt
import numpy as np
import ast
from wrap_up import string_process as sp
from nltk.corpus import stopwords
import ast
import pandas as pd

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def get_headlines(f, c=0):
    TOT = []
    for line in f.readlines():
        name = line.split(",")
        headlines = name[-100:]
        for l in headlines:
            if l.replace('"', '') == 'Travel':
                print(headlines)
            if l not in TOT:
                TOT.append(l.replace('\n', ''))
    return TOT

def yesno (TOT):
    vec_yesno = []
    for r in range(len(TOT)):
        row = TOT[r]
        vec_yesno.append([row, int(0), int(0)])
    return vec_yesno

def fill_yesno (f, vec_yesno, TOT, d=0, e=0):
    vec_yesno = np.asarray(vec_yesno)
    for line in f.readlines():
        name = line.split(",")
        headlines = name[-100:]
        results = name[17:-101]
        headcount = 0
        for k in range(len(results) - 5):
            if not isfloat(results[k]):
                if results[k]== 'Yes':
                    d+=1
                    h = headlines[headcount].replace('\n', '')
                    ind = TOT.index(h)
                    c = int(vec_yesno[ind, 1])
                    c += 1
                    vec_yesno[ind, 1] = c
                    headcount += 1
                if results[k] == 'No':
                    d+=1
                    h = headlines[headcount].replace('\n', '')
                    ind = TOT.index(h)
                    c = int(vec_yesno[ind, 2])
                    c += 1
                    vec_yesno[ind, 2] = c
                    headcount += 1
    print(d)
    return vec_yesno

def removenull (filledyesno):
    nonull = []
    for k in range(len(filledyesno)):
        y = int(filledyesno[k, 1])
        n = int(filledyesno[k, 2])
        if y+n != 0:
            nonull.append([filledyesno[k,0],filledyesno[k,1], filledyesno[k,2]])
    return nonull

def labels (vec_yesno):
    label = []
    for row in vec_yesno :
        st = row[0]
        word = ""
        st = sp.string_precess(st)
        if (st not in stopword and st is not ''):
            word = word + str(st)
            yes = row[1]
            no = row[2]
            if yes >= no :
                label.append([row[0], word, 1])
            if yes < no :
                label.append([row[0], word, 0])
    return np.asarray(label)

def hist_freqlab(filledyesno):
    dist = []
    for k in range(len(filledyesno)):
        y = int(filledyesno[k, 1])
        n = int(filledyesno[k, 2])
        dist.append(y + n)
    dist = np.asarray(dist)
    plt.hist(dist, bins=np.arange(dist.min(), dist.max() + 1) - 0.5)
    plt.title('Frequency of labels per headline (Avg:9.98)')
    plt.savefig('freq_labels.png')

def labeled (vec_yesno):
    label_ed = []
    for row in vec_yesno:
        label_ed.append([row[1], 0])
    for i in range (len(vec_yesno)):
        yes = vec_yesno[i,1]
        no = vec_yesno[i, 2]
        sum = yes + no
        label_ed[i][1] = sum
    return label_ed

stopword = set(stopwords.words('english'))

def to_classify (g):
    toclass = []
    for line in g.readlines():
        row = line.split('"')
        if len(row) == 3:
            two = row[0].split(',')
            word = ""
            st = two[6]
            st = sp.string_precess(st)
            if (st not in stopword and st is not ''):
                word = word + str(st)
            toclass.append(two[6])
    return np.asarray(toclass)

def test_set(toclass, labels):
    toclasss = []
    claa = np.asarray(list(set(toclass)-set(labels)))
    for line in claa :
        word = ""
        st = line
        st = sp.string_precess(st)
        if (st not in stopword and st is not ''):
            word = word + str(st)
        toclasss.append([line, word, 0])
    return np.asarray(toclasss)

def topic_matrix(TOT, f, topics):
    d_prim = pd.DataFrame(0, columns=topics, index=TOT)
    d_sec = pd.DataFrame(0, columns=topics, index=TOT)
    for line in f.readlines():
        name = line.split(",")
        headlines = name[-100:]
        results = name[17:-101]
        headcount = 0
        for k in range(len(results) - 5):
            h = headlines[headcount].replace('\n', '')
            ind = TOT.index(h)
            if results[k] != "Yes" and results[k] != "No":
                if results[k].replace('"', '') in topics:
                    if not isfloat(results[k]):
                        if '"' not in results[k]:
                            dp = d_prim[str(results[k])]
                            dp[ind]+=1
                        if '"' in results[k]:
                            if results[k].startswith('"'):
                                if results[k].replace('"', '')==results[k+3]:
                                    dp = d_prim[str(results[k].replace('"', ''))]
                                    dp[ind]+=1
                                    ds = d_sec[str(results[k+1].replace('"', ''))]
                                    ds[ind]+=1
                                if results[k+1].replace('"', '') == results[k + 2]:
                                    dp = d_prim[str(results[k+1].replace('"', ''))]
                                    dp[ind] += 1
                                    ds = d_sec[str(results[k].replace('"', ''))]
                                    ds[ind] += 1
            else :
                headcount += 1
    d_prim = d_prim.div(d_prim.sum(axis=1), axis=0)
    d_prim = d_prim.multiply(100)
    d_sec = d_sec.div(d_sec.sum(axis=1), axis=0)
    d_sec = d_sec.multiply(100)
    return d_prim, d_sec

def topic_matrix_pol(d_prim):
    d_primprim = pd.DataFrame(columns=['raw', 'message',"label"], index=d_prim.index)
    d1 = d_prim["Politics"]
    d2 = d_prim.loc[:, d_prim.columns != "Politics"]
    d2["Max_Val"] = d2.max(axis=1)
    d2["Mean_Val"] = d2.mean(axis=1)
    for row in d_primprim.index:
        st = row
        word = ""
        st = sp.string_precess(st)
        if (st not in stopword and st is not ''):
            word = word + str(st)
            d_primprim.loc[row, 'raw'] = str(row)
            d_primprim.loc[row, 'message'] = str(word)
        if d1.loc[row] >= d2.loc[row, "Mean_Val"]:
            d_primprim.loc[row, 'label'] = 1
        else:
            d_primprim.loc[row, 'label'] = 0
    return d_primprim



