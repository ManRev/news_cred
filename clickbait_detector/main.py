from clickbait_detector.svm import *
from clickbait_detector.clickbait_publisher import *
import clickbait_detector.create_matrix as CM
import numpy as np

year = "2018"

# /// Publishers of interest for the PUB. DIET
target = ["www.theatlantic.com",  "www.cnbc.com",
          "www.usatoday.com", "www.huffingtonpost.com","www.foxnews.com", "www.forbes.com",
          "www.washingtonpost.com", "www.cnn.com"]
tt = []
for url in target:
    domain = url.split(".")
    tt.append(domain[1])
target = tt

# //// Reduce at the same pool of Publishers for Both analysis
common_publi = ["cnn","foxnews","huffingtonpost","theatlantic",
"nypost","usatoday",
"washingtonpost","wsj", "latimes",
"chicagotribune", "seattletimes", "denverpost"]

# ////Locations
proxy = ["172.241.135.167:20875", "45.32.231.36:31280", "69.28.85.89:31280", "185.12.6.81:31280", "104.236.235.221:31280",
"104.36.17.62:31280", "18.30.67.14:8080", "173.230.133.30:31280"]
location = ["Boston", "Seattle", "Houston", "San Jose", "New York", "Miami", "Cambridge", "Atlanta"]

topics = ["Politics", "Education", "Personal Finance", "Healthcare", "Technology", "Sports", "Entertainment",
          "Culture/Religion", "Romance/Dating", "Retail", "Local News", "Other"]

if year == '2016':
    testData = pd.read_pickle("path2016.pickle")
    testData_unique = testData.drop_duplicates(subset=["Text"], keep='first')
    testData = testData.loc[testData["URLfrom"].isin(common_publi)]

if year == "2018":
    testData = pd.read_pickle("path2018.pickle")
    testData_unique = testData.drop_duplicates(subset=["Text"], keep='first')
    print(testData["URLfrom"].drop_duplicates())
    testData["URLfrom"].drop_duplicates().to_csv("publishers2018.csv")
mat = []
mat_url = []

### SET THE CRNS
testData_ads = testData.loc[testData["Type"]=="ads"]
testData_recs = testData.loc[testData["Type"]=="recs"]
testData_unique_ads = testData_unique.loc[testData_unique["Type"]=="ads"]
testData_unique_recs = testData_unique.loc[testData_unique["Type"]=="recs"]

testData_cb = testData.loc[testData['Label_Clickbait']==1]
testData_unique_cb = testData_unique.loc[testData_unique['Label_Clickbait']==1]

testData_ads_cb = testData.loc[(testData["Type"]=="ads") & (testData['Label_Clickbait']==1)]
testData_recs_cb = testData.loc[(testData["Type"]=="recs") & (testData['Label_Clickbait']==1)]
testData_unique_ads_cb = testData_unique.loc[(testData_unique["Type"]=="ads") & (testData_unique['Label_Clickbait']==1)]
testData_unique_recs_cb = testData_unique.loc[(testData_unique["Type"]=="recs") & (testData_unique['Label_Clickbait']==1)]

# //// GENERAL STATISTICS
print(year)
print("OVERALL RESULTS")
print("Number of headlines in the dataset: ", len(testData), "among which are unique", len(testData_unique))
print("Percentage of unique headlines: ", len(testData_unique)/len(testData))
print("Percentage of ads (among unique): ", len(testData_unique_ads)/len(testData_unique))
print("Percentage of recs (among unique): ", len(testData_unique_recs)/len(testData_unique))
print("--------------------------------------------------------")
print("--------------------------------------------------------")

print("OVERALL CLICKBAIT RESULTS")
print("Percentage of clickbait: ", len(testData_cb)/len(testData))
print("Percentage of clickbait: ", testData["Label_Clickbait"].mean())
print("Percentage of clickbait (unique): ", len(testData_unique_cb)/len(testData_unique))
print("Percentage of clickbait (ads): ", len(testData_unique_ads_cb)/len(testData_unique_ads))
print("Percentage of clickbait (recs): ", len(testData_unique_recs_cb)/len(testData_unique_recs))
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print(len(testData_unique_cb),len(testData_unique), len(testData_unique_ads_cb), len(testData_unique_ads), len(testData_unique_recs_cb), len(testData_unique_recs) )
for top in topics:
    print(top)
    print("OVERALL ", top, " RESULTS")
    testData_topic = testData_unique.loc[testData_unique[top] == 1]
    testData_topic_ads = testData_topic.loc[testData_topic["Type"] == "ads"]
    testData_topic_recs = testData_topic.loc[testData_topic["Type"] == "recs"]
    testData_topic_cb = testData_unique.loc[(testData_unique[top] == 1) & (testData_unique['Label_Clickbait'] == 1)]
    print("Percentage of " + top + " (unique): " + str(len(testData_topic) / len(testData_unique)))
    print("Percentage of " + top + " (ads): " + str(len(testData_topic_ads) / len(testData_unique_ads)))
    print("Percentage of " + top + " (recs): " + str(len(testData_topic_recs) / len(testData_unique_recs)))
    if len(testData_topic) != 0:
        print("Percentage of clickbait and " + top + " (unique): " + str(len(testData_topic_cb) / len(testData_topic)))
    print("--------------------------------------------------------")

print("********************************************************")
print("--------------------------------------------------------")
print("********************************************************")

# //// STATISTICS FOR THE TWO BIGGEST CRNs
print("CRN CLICKBAIT RESULTS:")
print("Number of headilnes from Taboola:", len(testData_unique.loc[testData_unique['CRN']=="taboola"]))
print("Percentage of clickbait (unique) in Taboola : ",
      len(testData_unique.loc[(testData_unique['CRN']=="taboola") & (testData_unique['Label_Clickbait']==1)])/
      len(testData_unique.loc[testData_unique['CRN']=="taboola"]))
print("Percentage of clickbait (ads) in Taboola : ",
      len(testData_unique.loc[(testData_unique['CRN']=="taboola") & (testData_unique['Label_Clickbait']==1) & (testData_unique['Type']=="ads")])/
      len(testData_unique.loc[(testData_unique['CRN']=="taboola") & (testData_unique['Type']=="ads")]))

print("Percentage of clickbait (recs) in Taboola : ",
      len(testData_unique.loc[(testData_unique['CRN']=="taboola") & (testData_unique['Label_Clickbait']==1) & (testData_unique['Type']=="recs")])/
      len(testData_unique.loc[(testData_unique['CRN']=="taboola") & (testData_unique['Type']=="recs")]))
array = testData_unique.loc[testData_unique['CRN']=="taboola"]
array = array["Label_Clickbait"].values
#print(np.std(array))
print("Number of headilnes from Outbrain:", len(testData_unique.loc[testData_unique['CRN']=="outbrain"]))
print("Percentage of clickbait (unique) in Outbrain : ",
      len(testData_unique.loc[(testData_unique['CRN']=="outbrain") & (testData_unique['Label_Clickbait']==1)])/
      len(testData_unique.loc[testData_unique['CRN']=="outbrain"]))
print(
    "Percentage of clickbait (ads) in Outbrain : ",
      len(testData_unique.loc[(testData_unique['CRN']=="outbrain") & (testData_unique['Label_Clickbait']==1) & (testData_unique['Type']=="ads")])/
      len(testData_unique.loc[(testData_unique['CRN']=="outbrain") & (testData_unique['Type']=="ads")])
)
print(
    "Percentage of clickbait (recs) in Outbrain : ",
      len(testData_unique.loc[(testData_unique['CRN']=="outbrain") & (testData_unique['Label_Clickbait']==1) & (testData_unique['Type']=="recs")])/
      len(testData_unique.loc[(testData_unique['CRN']=="outbrain") & (testData_unique['Type']=="recs")])
)
array = testData_unique.loc[testData_unique['CRN']=="outbrain"]
array = array["Label_Clickbait"].values
print("--------------------------------------------------------")
print("--------------------------------------------------------")

for top in topics:
    print("CRN ", top, " RESULTS")
    print("Percentage of " + top + " (unique): in Taboola: " + str(
        len(testData_unique.loc[(testData_unique['CRN']=="taboola") & (testData_unique[top]==1)])/
      len(testData_unique.loc[testData_unique['CRN']=="taboola"])))
    array = testData_unique.loc[testData_unique['CRN'] == "taboola"]
    array = array[top].values
    print("Percentage of clickbait (ads) in Taboola : ",
          len(testData_unique.loc[(testData_unique['CRN'] == "taboola") & (testData_unique[top] == 1) & (
          testData_unique['Type'] == "ads")]) /
          len(testData_unique.loc[(testData_unique['CRN'] == "taboola") & (testData_unique['Type'] == "ads")]))
    #print(np.std(array))
    print("Percentage of " + top + " (unique): in Outbrain: " + str(
        len(testData_unique.loc[(testData_unique['CRN'] == "outbrain") & (testData_unique[top] == 1)]) /
        len(testData_unique.loc[testData_unique['CRN'] == "outbrain"])))
    array = testData_unique.loc[testData_unique['CRN'] == "outbrain"]
    array = array[top].values
    print(
        "Percentage of clickbait (unique) in Outbrain : ",
        len(testData_unique.loc[(testData_unique['CRN'] == "outbrain") & (testData_unique[top] == 1) & (
        testData_unique['Type'] == "ads")]) /
        len(testData_unique.loc[(testData_unique['CRN'] == "outbrain") & (testData_unique['Type'] == "ads")])
    )
    print("--------------------------------------------------------")


print("********************************************************")
print("--------------------------------------------------------")
print("********************************************************")
print(testData_unique['Proxy'])
# //// STATISTICS PER LOCATION
if year == "2018":
    print("LOCATION CLICKBAIT and TOPICAL RESULTS:")
    for pro in range (len(proxy)):
        loc = proxy[pro]
        testData_prox = testData_unique.loc[testData_unique['Proxy']==loc]
        print("In ", location[pro])
        print("Nuumber of headlines in this location:", len(testData_prox))
        print("Percentage of clickbait (unique): ", len(testData_prox.loc[testData_prox["Label_Clickbait"]==1])/len(testData_prox))
        for top in topics:
            print("Percentage of ", top, ": ",
                  len(testData_prox.loc[testData_prox[top] == 1]) / len(testData_prox))
    print("--------------------------------------------------------")

print("********************************************************")
print("--------------------------------------------------------")
print("********************************************************")


# //// STATISTICS PER PUBLISHER
for targeted in target:
    testData_publi = testData_unique.loc[testData_unique['URLfrom'] == targeted]
    print("TYPOLOGY for ", targeted)
    print("Numbr of headlines from this source:", len(testData_publi))
    print("Percentage of unique headlines: ", len(testData_publi)/len(testData.loc[testData['URLfrom'] == targeted]))
    if len(testData_publi) != 0:
        print("Percentage of ads: ", len(testData_publi.loc[testData_publi["Type"]=="ads"])/len(testData_publi))
        print("Percentage of recs: ", len(testData_publi.loc[testData_publi["Type"]=="recs"])/len(testData_publi))
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    print("PER PUBLISHER RESULTS ", targeted)
    if len(testData_publi) != 0 :
        print("Percentage of clickbait (unique): ", len(testData_publi.loc[testData_publi["Label_Clickbait"]==1])/len(testData_publi))
    if len(testData_publi.loc[testData_publi["Type"] == "ads"]) != 0:
        print("Percentage of clickbait (unique) ads: ",
          len(testData_publi.loc[(testData_publi["Type"] == "ads") & (testData_publi["Label_Clickbait"]==1)]) /
          len(testData_publi.loc[testData_publi["Type"] == "ads"]))
    array = testData_publi.loc[testData_publi["Type"] == "ads"]
    array = array["Label_Clickbait"]
    if len(testData_publi.loc[testData_publi["Type"] == "recs"]) != 0:
        print("Percentage of clickbait (unique) recs: ",
          len(testData_publi.loc[(testData_publi["Type"] == "recs") & (testData_publi["Label_Clickbait"]==1)]) /
          len(testData_publi.loc[testData_publi["Type"] == "recs"]))
    array = testData_publi.loc[testData_publi["Type"] == "recs"]
    array = array["Label_Clickbait"]
    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
    for top in topics:
        if len(testData_publi) != 0:
            print("Percentage of ", top, "(unique): ", len(testData_publi.loc[testData_publi[top]==1])/len(testData_publi))
        if len(testData_publi.loc[testData_publi[top]==1]) != 0:
            print("Percentage of cliackbait and ", top, "(unique): ",
              len(testData_publi.loc[(testData_publi[top]==1) & (testData_publi["Label_Clickbait"] == 1)]) /
              len(testData_publi.loc[testData_publi[top]==1]))
            array = testData_publi.loc[testData_publi[top]==1]
            array = array["Label_Clickbait"]
        if len(testData_publi) != 0 :
            print("Percentage of ", top, " (unique) ads: ", len(
                testData_publi.loc[(testData_publi["Type"] == "ads") & (testData_publi[top] == 1)]) / len(
                testData_publi.loc[testData_publi["Type"]=='ads']))
            array = testData_publi.loc[testData_publi["Type"] == "ads"]
            array = array[top]
            if len(
                testData_publi.loc[testData_publi["Type"]=='recs']) != 0:
                print("Percentage of ", top, " (unique) recs: ", len(
                    testData_publi.loc[(testData_publi["Type"] == "recs") & (testData_publi[top] == 1)]) / len(
                    testData_publi.loc[testData_publi["Type"]=='recs']))
            array = testData_publi.loc[testData_publi["Type"] == "recs"]
            array = array[top]
        print("--------------------------------------------------------")

print("********************************************************")
print("--------------------------------------------------------")
print("********************************************************")

count_overlap = []*len(topics)
for top in topics:
    count = 0
    overlap = testData_unique.loc[testData_unique["Politics"]==1]
    overlap = overlap.loc[overlap[top] == 1]

    count_overlap.append(len(overlap))
print("Overlap with political topic is:")
for i in range (len(count_overlap)):
    print(topics[i], " :", count_overlap[i])

test_top = testData_unique[["Politics", "Education", "Personal Finance", "Healthcare", "Technology", "Sports",
                            "Entertainment","Culture/Religion", "Romance/Dating", "Retail", "Local News", "Other"]]

test_top = test_top.sum(axis=1)
val = test_top.value_counts()
val = val.div(0.01*val.sum())
print(val)

