from clickbait_detector.svm import *
from clickbait_detector.clickbait_publisher import *


path = '/Users/Manon/Desktop/Current/Projects/CRN/external_data/TrainingSet_5000.csv'

f = open(path, 'r')
g = open('/Users/Manon/Desktop/Current/Projects/CRN/wrap_up/all_logs_english_excl_ids.csv', 'r')

headlines = CM.get_headlines(f)
print(len(headlines))
yesno = CM.yesno(headlines)
f = open(path, 'r')
filledyesnonull = CM.fill_yesno(f, yesno, headlines)
filledyesno = CM.removenull(filledyesnonull)

#print(filledyesno[:-20])
filledyesno = filledyesno[:-20]

filledyesno = np.asarray(filledyesno)
#Plot distribution of labels
#CM.hist_freqlab(filledyesno)

training = CM.labels(filledyesno)
#print(training)
#print(training.shape)

test = CM.to_classify(g)
#svm.vizu(test)
#print(test.shape)

test = CM.test_set(test, training[:,0])
#print(test.shape)

headers_train = ['raw', 'message', 'label']
trainData = pd.DataFrame(training, columns=headers_train)
print(trainData.shape)

headers_test = ['raw', 'message', 'label']
testData = pd.DataFrame(test, columns=headers_test)
#print(testData)

p_spam = train(trainData)[0]
p_notSpam = train(trainData)[1]
positiveTotal = train(trainData)[2]
negativeTotal = train(trainData)[3]
# (2592, 2225, 4817, 0.5380942495329043, 0.4619057504670957)
print(p_spam, p_notSpam, positiveTotal, negativeTotal)

#//// TEST
#email = "donald"
#spam = True
#print(conditionalWord("donald", spam, positiveTotal, negativeTotal))
#print(conditionalEmail(email, spam, positiveTotal, negativeTotal))
#print(classify(email, p_spam, p_notSpam, positiveTotal, negativeTotal))
#////

numSpam_test = 0
tot_test = 0
alpha = 0.1

#//// LABEL THE TEST DATA
for index, row in testData.iterrows():
    cl = classify(row['message'], p_spam, p_notSpam, positiveTotal, negativeTotal, alpha)
    if cl == 1 :
        row['label'] = cl
        numSpam_test += 1
    tot_test += 1
#print(testData)
#print('Alpha is 0.1:')
#print(numSpam_test)
#print(numSpam_test/77916)
#////

#//// CROSS VALIDATION
pred = cross_validationA(trainData, alpha)
print(cross_validationA(trainData, alpha))

print(ROC(trainData, pred, "plots/ROC_clickbaitdetector.png"))
#////

#//// Test Whether There is A Need to Keep Stop Words
#interestion_dictionaries(trainPositive, trainNegative)
#////

#open_all_path = "/Users/Manon/Desktop/Current/Projects/CRN/dataset/all_logs_combined_recs_and_ads.txt"
open_all_path = "/Users/Manon/Desktop/Current/Projects/CRN/wrap_up/all_logs_english_excl_ids.csv"
dict_tot = open_all_com(open_all_path)

publishers = list(set(dict_tot['publisher']))
#print(testData)
#print(testData.keys())

#////TEST
#head = "16 Hilarious Home Mowing Fails YOU Wont Believe"
#print(head in testData['raw'])
#ind = testData[testData['raw']==head].index.values.astype(int)[0]
#print(ind)
#print(testData.ix[ind])
#////

#word_diet(dict_tot, testData)
yai = list(map(int,testData['label']))
print('spam=', sum(yai))
print("tot=", len(yai))
#publishers_diet(dict_tot, testData, publishers, "clickbait_publihsers.csv")


