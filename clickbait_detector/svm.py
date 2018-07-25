import nltk
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import WordCloud, STOPWORDS
from math import log, sqrt
from wrap_up import string_process as sp
import pandas as pd
import numpy as np
from clickbait_detector import create_matrix as CM
from sklearn import metrics
from sklearn import model_selection


#%matplotlib inline

stopwords= set(STOPWORDS)
new_words = ['new', "best"]
new_stopwords=stopwords.union(new_words)

def vizu(training):
    #clickbait_words = ' '.join(list(training[training[:,2] == str(0)][:,1]))
    #clickbait_words = ' '.join(list(training[training[:, 2] == str(1)][:,1]))
    clickbait_words = ' '.join(list(training))
    clickbait_wc = WordCloud(width=512, height=512, stopwords=stopwords, max_words=120).generate(clickbait_words)
    plt.figure(figsize=(10,8), facecolor='k')
    plt.imshow(clickbait_wc)
    plt.axis('off')
    plt.tight_layout(pad = 0)
    plt.savefig('test_wordcloud4')

trainPositive = dict()
trainNegative = dict()


def train(trainData):
    total = 0
    numSpam = 0
    for index, row in trainData.iterrows():
        label = int(row['label'])
        headline = row['message']
        #print(label, headline)
        if int(label) == 1:
            numSpam += 1
        total += 1
        processEmail(headline, label)
    pA = numSpam/total
    pNotA = (total - numSpam)/total
    positiveTotal = len(trainPositive)
    negativeTotal = len(trainNegative)
    #print(len(trainPositive), len(trainNegative))
    return pA, pNotA, positiveTotal, negativeTotal


def processEmail(headline, label):
    for word in headline.split():
        if label == 1:
            trainPositive[word] = trainPositive.get(word, 0) + 1
        else:
            trainNegative[word] = trainNegative.get(word, 0) + 1

"""
def conditionalWord(word, spam, positiveTotal, negativeTotal):
    if spam:
        if word in trainPositive:
            return trainPositive[word]/positiveTotal
    if word in trainNegative:
        return trainNegative[word]/negativeTotal
    return 0
"""


def conditionalWord(word, spam, positiveTotal, negativeTotal, alpha, numWords):
    if spam:
        return (trainPositive.get(word,0)+alpha)/(positiveTotal+alpha*numWords)
    return (trainNegative.get(word, 0) + alpha) / (negativeTotal + alpha * numWords)


def conditionalEmail(headline, spam, positiveTotal, negativeTotal, alpha):
    result = 1.0
    numWords = len(headline.split())
    for word in headline.split():
        #print(word)
        result *= conditionalWord(word, spam, positiveTotal, negativeTotal, alpha, numWords)
    return result


def classify(email, pA, pNotA, positiveTotal, negativeTotal, alpha):
    isSpam = pA * conditionalEmail(email, True, positiveTotal, negativeTotal, alpha) # P (A | B)
    notSpam = pNotA * conditionalEmail(email, False, positiveTotal, negativeTotal, alpha) # P(¬A | B)
    #print(isSpam, notSpam)
    if isSpam == notSpam == 0 :
        print(email)
    if isSpam >= notSpam :
        return 1
    return 0

def classify_proba(email, pA, pNotA, positiveTotal, negativeTotal, alpha):
    isSpam = pA * conditionalEmail(email, True, positiveTotal, negativeTotal, alpha) # P (A | B)
    notSpam = pNotA * conditionalEmail(email, False, positiveTotal, negativeTotal, alpha) # P(¬A | B)
    #print(isSpam, notSpam)
    if isSpam == notSpam == 0 :
        print(email)
    return notSpam, isSpam


from nltk.corpus import stopwords
stop = stopwords.words('english')
def interestion_dictionaries(trainPositive, trainNegative):
    count = 0
    count_stop = 0
    for word in trainPositive:
        if word in trainNegative :
            count += 1
            if word in stop :
                count_stop +=1
                if trainPositive[word]/trainNegative[word] > 3:
                    print(word, trainPositive[word], trainNegative[word])
    print(count, count_stop)

def cross_validationA(trainData, alpha):
    s = trainData['label'].shape
    pred = np.zeros((s[0],2))
    X = np.array(trainData['message'])
    y = list(map(int, trainData['label']))
    y = np.array(y)
    folds = model_selection.StratifiedKFold(10)
    for tr, te in folds.split(X, y):
        # Restrict data to train/test folds
        Xtr = X[tr]
        Xte = X[te]
        p_spam = train(trainData)[0]
        p_notSpam = train(trainData)[1]
        positiveTotal = train(trainData)[2]
        negativeTotal = train(trainData)[3]
        predi =  []
        for i in range(len(Xte)):
            cl = classify_proba(Xte[i], p_spam, p_notSpam, positiveTotal, negativeTotal, alpha)
            predi.append(cl)
        pred[te]=predi
    return pred

def ROC(trainData, pred, title):
    y = list(map(int, trainData['label']))
    y = np.array(y)
    s = pred.shape
    y_tri = np.zeros((s[0],1))
    for i in range(len(pred)) :
        row = pred[i]
        if row[0] <= row[1]:
            y_tri[i]=1
    print("Accuracy:", metrics.accuracy_score(y, y_tri))
    print("Confusion matrix:", metrics.confusion_matrix(y, y_tri))
    # ROC curve
    fpr_logreg, tpr_logreg, thresholds = metrics.roc_curve(y, y_tri, pos_label=1)

    # Area under the ROC curve
    auc = metrics.auc(fpr_logreg, tpr_logreg)

    # Plot the ROC curve
    plt.plot(fpr_logreg, tpr_logreg, '-', color='orange', label='AUC = %0.3f' % auc)

    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)
    plt.title('Logisitc Regression', fontsize=16)
    plt.legend(loc="lower right")
    plt.savefig(title)