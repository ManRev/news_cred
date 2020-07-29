from clickbait_detector.svm import *
from clickbait_detector.clickbait_publisher import *
import clickbait_detector.create_matrix as CM
import numpy as np


year, year_ts = "2018", "2018"
print("TOTAL")

# ////DATA 2018 path:
if year == "2018":
    g_2018 = open("raw2018data.txt", 'r')
    testData = CM.to_classify(g_2018, int(year))

if year_ts == "2018":
    path ='trainingMarch.csv'

# ////DATA 2016 path:
if year == "2016":
    g_2016 = open("raw2016data.txt")
    testData = CM.to_classify(g_2016, int(year))

if year_ts == "2016":
    path = 'TrainingSet_5000.csv'

# ////BUILD TRAINING SET FOR CLICKBAIT DETECTOR
f = open(path, 'r')
headlines = CM.get_headlines(f)
yesno = CM.yesno(headlines)
f = open(path, 'r')
filledyesnonull = CM.fill_yesno(f, yesno, headlines)
filledyesno = CM.removenull(filledyesnonull)
filledyesno = filledyesno[:-20]
filledyesno = np.asarray(filledyesno)
training = CM.labels(filledyesno)

trainPositive = dict()
trainNegative = dict()

# ////Training Set CLICKBAIT
headers_train = ['raw', 'message', 'label']
trainData = pd.DataFrame(training, columns=headers_train)
train2 = train(trainData)
p_spam = train2[0]
p_notSpam = train2[1]
positiveTotal = train2[2]
negativeTotal = train2[3]
print(p_spam, p_notSpam, positiveTotal, negativeTotal)

numSpam_test = 0
tot_test = 0
alpha = 0.1

pred = cross_validationA(trainData, alpha, train2[4], train2[5])
print(ROC(trainData, pred, "plots/ROC_clickbait_2018.png"))

testData = testData.loc[testData["Text_sp"]!=""]
testData = testData.loc[testData["Text_sp"]!=" "]
testData = testData.drop_duplicates(subset=["Text"], keep='first')
testData = testData['Text_sp'].replace('', np.nan, inplace=True)
testData = testData.dropna(subset=['Text_sp'], inplace=True)


# //// LABEL TEST SET
i = 0
for index, row in testData.iterrows():
    i += 1
    cl = classify(row['Text_sp'], p_spam, p_notSpam, positiveTotal, negativeTotal, alpha, train2[4], train2[5], 5)
    if cl == 1 and row['Text_sp'] is not "":
        testData.at[index, "Label_Clickbait"] = 1
        numSpam_test += 1
    tot_test += 1

# ////Training Set TOPICAL
topics = ["Politics", "Education", "Personal Finance", "Healthcare", "Technology", "Sports", "Entertainment",
          "Culture/Religion", "Romance/Dating", "Retail", "Local News", "Other"]

#//// BINARY CLASSIFICATION AND TRAINING
f = open(path, 'r')
headlines = list(set(CM.get_headlines(f)))
f = open(path, 'r')
d = []
if year_ts == "2016":
    d = CM.topic_matrix(headlines, f, topics)
if year_ts == "2018":
    d = CM.topic_matrix_2018(headlines, f, topics)
d_prim = d[0]
d_sec = d[1]
print("Representation of the topics in the training set", CM.count_top(d_prim, topics))

for top in topics:
    binary_pol_prim = CM.topic_matrix_pol(d_prim, d_sec, top)
    trainData = binary_pol_prim.iloc[1:]
    train3 = train(trainData)
    p_spam = train3[0]
    p_notSpam = train3[1]
    positiveTotal = train3[2]
    negativeTotal = train3[3]
    numSpam_test = 0
    tot_test = 0
    alpha = 0.1

    # //// LABEL TEST SET
    i = 0
    for index, row in testData.iterrows():
        i += 1
        cl = classify(row['Text_sp'], p_spam, p_notSpam, positiveTotal, negativeTotal, alpha, train3[4], train3[5])
        if cl == 1 and row['Text_sp'] is not "":
            testData.at[index, top]=1
            numSpam_test += 1
        tot_test += 1
testData_unique = testData.drop_duplicates(subset=["Text"], keep='first')
