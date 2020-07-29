# news_cred

### **Code for scraping:** 
  - DataScraping.py to scrape CRNs' widgets (Outbrain, Taboola, Revcontent, Zergnet, Dianomi)
 
### **Code for supervised learning analysis:**

**Clickbait_detector** directory contains 5 files:
  - create_matrix.py transfomrs the raw english data into any format needed for the analyis. 
  - clickbait_detector.py contains the Bayes classifier coded. 
  - main_labeling.py converts the raw data into a labeled dataframe that asses whether headlines are clickbait and the headline's topics. Resuires create_matrix.py and clickbait_detector.py.
  - main.py allow to compute and print the data statistics from the dataframe created in main_labeling (can be run on the sampled data data_2018_delt5_all.pickle with year = 2018).
 
**Data** data used in the cickbait_dector and output:
  - TrainingSet_5000.csv is the training set for 2016 data collection.
  - trainingMarch.pcsv is the training set for 2018 data collection. 
  - test_scatterplot_2016_5max.pickle is the data output after running the Bayes Detector on 2016 raw data. 
  - test_scatterplot_2018_5max.pickle is the data output after running the Bayes Detector on 2018 raw data.
  - For raw data of both years, please reach out to us at mrevel@mit.edu! 
