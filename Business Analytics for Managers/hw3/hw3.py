# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 22:19:57 2021

@author: ipekh
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans

telcoCsvDataFrame = pd.read_csv("C:\\Users\\ipekh\\Desktop\\Big Data Homeworks\\Business Analytics for Managers\\hw3\\telco.csv")
telcoCsvDataFrame.columns = telcoCsvDataFrame.columns.str.lower()
telcoCsvDataFrame = telcoCsvDataFrame.drop("customerid", axis = 1)

numericTotalChargesErrorsCoerce = pd.to_numeric(telcoCsvDataFrame["totalcharges"], errors = "coerce")
telcoCsvDataFrame["totalcharges"] = numericTotalChargesErrorsCoerce.fillna(0)

columns = list(telcoCsvDataFrame.dtypes[telcoCsvDataFrame.dtypes == "object"].index)

for x in columns:
    telcoCsvDataFrame[x] = telcoCsvDataFrame[x].str.lower().str.replace(" ","")

telcoCsvDataFrame["churn"] = (telcoCsvDataFrame.churn == "yes").astype(int)

telcoCsvDataFrame.replace({"male" : 1, "female" : 0}, inplace = True)
telcoCsvDataFrame.replace("no_internet_service", "no", inplace = True)
telcoCsvDataFrame.replace("no_phone_service", "no", inplace = True)

booleanColumns = ["partner","dependents","phoneservice","multiplelines","onlinesecurity",
               "onlinebackup","deviceprotection","techsupport","streamingtv",
               "streamingmovies","paperlessbilling","churn"]

for x in booleanColumns:
    telcoCsvDataFrame[x].replace({"yes": 1, "no": 0}, inplace = True)


telcoCsvDataFrame = pd.get_dummies(data = telcoCsvDataFrame, columns = ["internetservice","contract","paymentmethod"])

yAxis = telcoCsvDataFrame["churn"]
xAxis = telcoCsvDataFrame.drop("churn", axis = 1)

trainingDataXAxisFully, testDataXAxis, trainingDataYAxisFully, testDataYAxis = train_test_split(xAxis, yAxis, test_size = .2)

trainingDataXAxis, xAxisValue, trainingDataYAxis, yAxisValue = train_test_split(trainingDataXAxisFully, trainingDataYAxisFully, test_size = .25)

logReg = LogisticRegression()
logReg.fit(trainingDataXAxis, trainingDataYAxis)

yAxisPrediction = logReg.predict(testDataXAxis)
accuracy_score(testDataYAxis, yAxisPrediction)

parameterDict = {"Param": [1, 5, 10, 20, 40]}

gridSearchResult = GridSearchCV(logReg, parameterDict)
gridSearchResult.fit(xAxisValue, yAxisValue)

maximumScoreAvailable = max(gridSearchResult.cvresults["mean_test_score"])
maximumScoreAvailableIndex = list(gridSearchResult.cvresults["mean_test_score"]).index(maximumScoreAvailable)
bestPossibleParamValue = parameterDict["Param"][maximumScoreAvailableIndex]

tunedLogisticRegression = LogisticRegression(C = bestPossibleParamValue, solver = "lbfgs", max_iter = 10000)
tunedLogisticRegression.fit(trainingDataXAxis, trainingDataYAxis)

tunedYAxisPrediction = tunedLogisticRegression.predict(testDataXAxis)
print(accuracy_score(testDataYAxis, tunedYAxisPrediction))

kmeans = KMeans(n_clusters = 2, random_state = 0).fit(trainingDataXAxis)

testDataXAxis["cluster"] = kmeans.predict(testDataXAxis)
trainingDataXAxis["cluster"] = kmeans.labels

clusteredLogisticRegression = LogisticRegression(C = 10, solver = "lbfgs", max_iter = 10000)
clusteredLogisticRegression.fit(trainingDataXAxis, trainingDataYAxis)

clusteredYAxisPrediction = clusteredLogisticRegression.predict(testDataXAxis)