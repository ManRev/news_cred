import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn import model_selection

## This code was originally written by Yerassyl.
## It can be found at https://gist.github.com/Yerazhas/077a743723644213f93f59b70fd3af3b
## It was partially updated to serve this research purpose.

def train(trainData):
    trainPositive = dict()
    trainNegative = dict()
    total = 0
    numSpam = 0
    for index, row in trainData.iterrows():
        label = int(row['label'])
        headline = row['message']
        if int(label) == 1:
            numSpam += 1
        total += 1
        processEmail(headline, label, trainPositive, trainNegative)
        trainPositive = processEmail(headline, label, trainPositive, trainNegative)[0]
        trainNegative = processEmail(headline, label, trainPositive, trainNegative)[1]
    pA = numSpam/total
    pNotA = (total - numSpam)/total
    positiveTotal = len(trainPositive)
    negativeTotal = len(trainNegative)
    return pA, pNotA, positiveTotal, negativeTotal, trainPositive, trainNegative


def processEmail(headline, label, trainPositive, trainNegative):
    if headline is not float:
        try :
            headline.split()
            for word in headline.split():
                if label == 1:
                    trainPositive[word] = trainPositive.get(word, 0) + 1
                else:
                    trainNegative[word] = trainNegative.get(word, 0) + 1
        except:
            print("oh")
    return(trainPositive, trainNegative)

def conditionalWord(word, spam, positiveTotal, negativeTotal, alpha, numWords, trainPositive, trainNegative):
    numm = numWords
    if spam:
        return (trainPositive.get(word, 0) + alpha) / (positiveTotal + alpha * numm)
    return (trainNegative.get(word, 0) + alpha) / (negativeTotal + alpha * numm)



def conditionalEmail(headline, spam, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative):
    result = 1.0
    numWords = len(headline.split())
    for word in headline.split():
        result *= conditionalWord(word, spam, positiveTotal, negativeTotal, alpha, numWords, trainPositive, trainNegative)
    return result


def classify(email, pA, pNotA, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative, lambda1):
    isSpam = pA * conditionalEmail(email, True, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative) # P (A | B)
    notSpam = pNotA * conditionalEmail(email, False, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative) # P(¬A | B)
    if isSpam == notSpam == 0 :
        print(email)
        return 0
    # Un-uncomment if binary classification
    else:
        ma = max(isSpam, notSpam)
        mi = min(isSpam, notSpam)
        if ma/mi > lambda1:
            if isSpam >= notSpam :
                return 1, isSpam/notSpam
            return 0, isSpam/notSpam
        return -1, isSpam/notSpam
    #return 0
    #return [isSpam, notSpam]

def classify_proba(email, pA, pNotA, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative):
    isSpam = pA * conditionalEmail(email, True, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative) # P (A | B)
    notSpam = pNotA * conditionalEmail(email, False, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative) # P(¬A | B)
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

def cross_validationA(trainData, alpha, trainPositive, trainNegative):
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
        tt = train(trainData)
        p_spam = tt[0]
        p_notSpam = tt[1]
        positiveTotal = tt[2]
        negativeTotal = tt[3]
        predi =  []
        for i in range(len(Xte)):
            cl = classify_proba(Xte[i], p_spam, p_notSpam, positiveTotal, negativeTotal, alpha, trainPositive, trainNegative)
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
    plt.close()