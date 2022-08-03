#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 19:59:15 2022

@author: aastha
"""

import numpy as np
import pandas as pd
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt
from pytorch_tabnet.tab_model import TabNetClassifier
from pandas import read_csv
from sklearn.impute import SimpleImputer


#load exonic data
data = read_csv('pipeline.csv')
df = data.copy()

for col in ['Function', 'LoF_HC_Canonical', 'Pfam_imp_domain', 'Outcome']:
    df[col] = df[col].astype('category')

ID = df['ID']
df = df.drop('ID', 1)    
    
#constant imputer
constant_imputer = SimpleImputer(strategy='constant', fill_value=-99)
df = constant_imputer.fit_transform(df)


#split into input and output columns
X, y = df[:, :-1], df[:, -1]

# load the model 
clf1_nopreproc = TabNetClassifier()
clf1_nopreproc.load_model("../wilsongenai_tabnet_model.zip")

loaded_preds = clf1_nopreproc.predict_proba(X)
op1 = pd.DataFrame(ID)
op2 = pd.DataFrame(clf1_nopreproc.predict(X))
op = op1.join(op2)
op.to_csv("predictions_tabnet", sep="\t")
