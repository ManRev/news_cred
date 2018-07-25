from clickbait_detector.svm import *
from clickbait_detector.clickbait_publisher import *

path = '/Users/Manon/Desktop/Current/Projects/CRN/external_data/TrainingSet_5000.csv'
f = open(path, 'r')
headlines = CM.get_headlines(f)
#print(len(headlines))
yesno = CM.yesno(headlines)

f = open(path, 'r')
filledyesnonull = CM.fill_yesno(f, yesno, headlines)
filledyesno = CM.removenull(filledyesnonull)
filledyesno = filledyesno[:-20]
filledyesno = np.asarray(filledyesno)
training = CM.labels(filledyesno)

g = open('/Users/Manon/Desktop/Current/Projects/CRN/wrap_up/all_logs_english_excl_ids.csv', 'r')
test = CM.to_classify(g)
test = CM.test_set(test, training[:,0])
headers_test = ['raw', 'message', 'label']
testData = pd.DataFrame(test, columns=headers_test)

f = open(path, 'r')
topics = ["Politics", "Education", "Personal Finance", "Healthcare", "Technology", "Sports", "Entertainment",
          "Culture/Religion", "Romance/Dating", "Retail", "Local News", "Other"]
headlines = list(set(CM.get_headlines(f)))

#//// BINARY CLASSIFICATION AND TRAINING
f = open(path, 'r')
d = CM.topic_matrix(headlines, f, topics)
d_prim = d[0]
d_sec = d[1]

binary_pol_prim = CM.topic_matrix_pol(d_prim)
#binary_pol_sec = CM.topic_matrix_pol(d_sec)

trainData = binary_pol_prim.iloc[1:]
#print(trainData)

p_spam = train(trainData)[0]
p_notSpam = train(trainData)[1]
positiveTotal = train(trainData)[2]
negativeTotal = train(trainData)[3]
# (2592, 2225, 4817, 0.5380942495329043, 0.4619057504670957)
#print(p_spam, p_notSpam, positiveTotal, negativeTotal)

numSpam_test = 0
tot_test = 0
alpha = 0.1

#//// CROSS VALIDATION
#pred = cross_validationA(trainData, alpha)
#print(cross_validationA(trainData, alpha))

#print(ROC(trainData, pred, "plots/ROC_politicaldetector.png"))
#////

#//// LABEL THE TEST DATA
for index, row in testData.iterrows():
    cl = classify(row['message'], p_spam, p_notSpam, positiveTotal, negativeTotal, alpha)
    if cl == 1 :
        row['label'] = cl
        numSpam_test += 1
    tot_test += 1
#open_all_path = "/Users/Manon/Desktop/Current/Projects/CRN/dataset/all_logs_combined_recs_and_ads.txt"
open_all_path = "/Users/Manon/Desktop/Current/Projects/CRN/wrap_up/all_logs_english_excl_ids.csv"
dict_tot = open_all_com(open_all_path)

publishers = list(set(dict_tot['publisher']))
#print(testData)
#print(testData.keys())

#//// NUMBER OF LABELED 1 IN THE TEST DATA
#word_diet(dict_tot, testData)
#yai = list(map(int,testData['label']))
#print('spam=', sum(yai))
#print("tot=", len(yai))
#publishers_diet(dict_tot, testData, publishers, "clickbait_publihsers_pol_sec.csv")

from skmultilearn.problem_transform import LabelPowerset
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# initialize Label Powerset multi-label classifier
# with a gaussian naive bayes base classifier
classifier = LabelPowerset(GaussianNB())

d_prim = d_prim[1:]
d_sec = d_sec[1:]
d_new = pd.DataFrame().reindex_like(d_prim)
d_new["index"] = d_new.index
s = d_prim.shape
d_primmean = d_prim.mean(axis=1)
for l in range (s[0]):
    for k in range (s[1]):
        if d_prim.iloc[l, k] >= d_primmean.iloc[l] :
            d_new.iloc[l, k] = int(1)
        else :
            d_new.iloc[l, k] = int(0)

# train
#X_train = np.array(d_new.index.tolist())
X_train = np.array(pd.DataFrame({ 'A' : range(1, s[0] + 1 )}))
y_train = np.array(d_new.loc[:, d_prim.columns != "index"])
print(X_train)
print("-------------")
print(y_train)
classifier.fit(X_train, y_train)

# predict
predictions = classifier.predict(X_train)
print(accuracy_score(y_train,predictions))

print("ADAPTED ALGORITHM")
from skmultilearn.adapt import MLkNN
classifier = MLkNN(k=20)
# train
classifier.fit(X_train, y_train)
# predict
predictions = classifier.predict(X_train)
print(accuracy_score(y_train,predictions))