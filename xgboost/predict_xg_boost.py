import xgboost as xgb
import pandas as pd
from pandas import read_csv
import numpy as np


#load exonic data
data = read_csv('pipeline.csv')
df = data.copy()

#create op_outcome file
op_outcome = df[['ID']].copy()
op_outcome["Outcome"] = ""
op_outcome.to_csv('op_outcome', sep="\t", index=False)

#drop ID column
ID = df['ID']
df = df.drop('ID', 1)   

#split into input and output columns
X, y = df.iloc[:, :-1], df.iloc[:, -1]

#load the model
model2 = xgb.XGBClassifier()
model2.load_model("wilsongenai_xg_boost_model.txt")
preds = model2.predict(X)

#save the predictions
df_preds = pd.DataFrame(preds)
df_preds.insert(0, 'ID', data['ID'])
header = ["ID", "Prediction"]
df_preds.columns = header
df_preds.to_csv("predictions_xgboost", index= False)
