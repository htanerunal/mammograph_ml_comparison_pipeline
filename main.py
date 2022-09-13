# This file is created to compare ML Classifiers with NLC
# Copyright (c) 2021 Hamit Taner Ünal and Prof.Fatih Başçiftçi

# Classification Task for Mammographic Mass Dataset

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import std, median
from numpy import mean
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, make_scorer, accuracy_score, RocCurveDisplay, auc
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict, cross_validate
import warnings
import logging

logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger('tensorflow').disabled = True
warnings.filterwarnings('ignore')

#Determine seed
seed = 7
np.random.seed(seed)

# Read data, exclude BI-RADS(non-predictive)
data = pd.read_csv("mammograph.csv",
                          names =['BI-RADS','Age','Shape','Margin','Density','Severity'],
                          usecols = ['Age','Shape','Margin','Density','Severity'],na_values='?')

# Print data summary
print(data.head())
print(data.info())

# Arrange Data, drop missing
data = data.dropna()
features = list(data.columns[:4])
X = data[features].values

labels = list(data.columns[4:])
y = data[labels].values
y = y.ravel()

# Print data summary
print(data.head())
print(data.info())

#Use seed to reproduce the results
print("Using seed ",seed)

# Define models to be used (with best hyperparameters)
model1 = LogisticRegression(C=1, max_iter=100, penalty='l2',solver='newton-cg')
model2 = RandomForestClassifier(n_estimators=400, criterion='entropy', max_depth=8, bootstrap = True, max_features = 'log2')
model3 = Sequential()
model3.add(Dense(9, input_dim=X.shape[1], activation='relu'))
model3.add(Dense(3, activation='relu'))
model3.add(Dense(1, activation="sigmoid"))
model3.compile(optimizer='Nadam', loss='binary_crossentropy', metrics=['accuracy'])
model4 = DecisionTreeClassifier(criterion='entropy',max_depth=5,max_features='log2',min_samples_leaf=9,min_samples_split=5)
model5 = GaussianNB(var_smoothing=0.43287612810830584)
model6 = KNeighborsClassifier(leaf_size=1, metric='minkowski',n_neighbors=19, p = 1,weights='distance')
model7 = SVC(C=10,gamma=0.01,kernel='rbf')

#Define model3 (ANN) as Keras Classifier
# Prepare for ANN
def create_ANN_model(optimizer='Nadam'):
    model = Sequential()
    model.add(Dense(9, input_dim=X.shape[1], activation='relu'))
    model.add(Dense(3, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

model3_keras = KerasClassifier(build_fn=create_ANN_model, verbose=0, epochs=150, batch_size=10)
model3_keras._estimator_type = "classifier"

# Define Stratified k-fold Cross Validation
kf = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)

# Initialize scores for each classifier
overall_score1 = []
overall_score2 = []
overall_score3 = []
overall_score4 = []
overall_score5 = []
overall_score6 = []
overall_score7 = []


# Start k-fold cross validation loop
csv1 = []
csv2 = []
csv3 = []
csv4 = []
csv5 = []
csv6 = []
csv7 = []

# Print Classification Reports
print("Classification Report for Logistic Regression:")
print("----------------------------------------------")
for score in [ "accuracy", "recall", "precision", "f1", "balanced_accuracy"]:
    steps = list()
    steps.append(('scaler', StandardScaler()))
    steps.append(('model', model1))
    pipeline = Pipeline(steps=steps)
    cv_score = cross_val_score(pipeline, X, y, scoring=score, cv=kf)
    print(score + " Mean: %.8f" % mean(cv_score) + " STD: %.8f" % std(cv_score) + " Median: %.8f" % median(cv_score))
    csv1.append(str(mean(cv_score)))
    csv1.append(str(std(cv_score)))
print("----------------------------------------------")

print("Classification Report for Random Forest:")
print("----------------------------------------------")
for score in [ "accuracy", "recall", "precision", "f1", "balanced_accuracy"]:
    steps = list()
    steps.append(('scaler', StandardScaler()))
    steps.append(('model', model2))
    pipeline = Pipeline(steps=steps)
    cv_score = cross_val_score(pipeline, X, y, scoring=score, cv=kf)
    print(score + " Mean: %.8f" % mean(cv_score) + " STD: %.8f" % std(cv_score) + " Median: %.8f" % median(cv_score))
    csv2.append(str(mean(cv_score)))
    csv2.append(str(std(cv_score)))
print("----------------------------------------------")

print("Classification Report for ANN:")
print("----------------------------------------------")
for score in [ "accuracy", "recall", "precision", "f1", "balanced_accuracy"]:
    steps = list()
    steps.append(('scaler', StandardScaler()))
    steps.append(('model', model3_keras))
    pipeline = Pipeline(steps=steps)
    cv_score = cross_val_score(pipeline, X, y, scoring=score, cv=kf)
    print(score + " Mean: %.8f" % mean(cv_score) + " STD: %.8f" % std(cv_score) + " Median: %.8f" % median(cv_score))
    csv3.append(str(mean(cv_score)))
    csv3.append(str(std(cv_score)))
print("----------------------------------------------")

print("Classification Report for CART:")
print("----------------------------------------------")
for score in [ "accuracy", "recall", "precision", "f1", "balanced_accuracy"]:
    steps = list()
    steps.append(('scaler', StandardScaler()))
    steps.append(('model', model4))
    pipeline = Pipeline(steps=steps)
    cv_score = cross_val_score(pipeline, X, y, scoring=score, cv=kf)
    print(score + " Mean: %.8f" % mean(cv_score) + " STD: %.8f" % std(cv_score) + " Median: %.8f" % median(cv_score))
    csv4.append(str(mean(cv_score)))
    csv4.append(str(std(cv_score)))
print("----------------------------------------------")

print("Classification Report for Naive Bayes:")
print("----------------------------------------------")
for score in [ "accuracy", "recall", "precision", "f1", "balanced_accuracy"]:
    steps = list()
    steps.append(('scaler', StandardScaler()))
    steps.append(('model', model5))
    pipeline = Pipeline(steps=steps)
    cv_score = cross_val_score(pipeline, X, y, scoring=score, cv=kf)
    print(score + " Mean: %.8f" % mean(cv_score) + " STD: %.8f" % std(cv_score) + " Median: %.8f" % median(cv_score))
    csv5.append(str(mean(cv_score)))
    csv5.append(str(std(cv_score)))
print("----------------------------------------------")

print("Classification Report for kNN:")
print("----------------------------------------------")
for score in [ "accuracy", "recall", "precision", "f1", "balanced_accuracy"]:
    steps = list()
    steps.append(('scaler', StandardScaler()))
    steps.append(('model', model6))
    pipeline = Pipeline(steps=steps)
    cv_score = cross_val_score(pipeline, X, y, scoring=score, cv=kf)
    print(score + " Mean: %.8f" % mean(cv_score) + " STD: %.8f" % std(cv_score) + " Median: %.8f" % median(cv_score))
    csv6.append(str(mean(cv_score)))
    csv6.append(str(std(cv_score)))
print("----------------------------------------------")

print("Classification Report for SVC:")
print("----------------------------------------------")
for score in [ "accuracy", "recall", "precision", "f1", "balanced_accuracy"]:
    steps = list()
    steps.append(('scaler', StandardScaler()))
    steps.append(('model', model7))
    pipeline = Pipeline(steps=steps)
    cv_score = cross_val_score(pipeline, X, y, scoring=score, cv=kf)
    print(score + " Mean: %.8f" % mean(cv_score) + " STD: %.8f" % std(cv_score) + " Median: %.8f" % median(cv_score))
    csv7.append(str(mean(cv_score)))
    csv7.append(str(std(cv_score)))
print("----------------------------------------------")
print("***** Printing CSV Data to export *************")
print(csv1)
print(csv2)
print(csv3)
print(csv4)
print(csv5)
print(csv6)
print(csv7)
print("******** End of CSV ***************************")

