import xgboost as xgb
from pandas import read_csv
import numpy as np


#load exonic data
data = read_csv('pipeline.csv')
df = data.copy()

ID = df['ID']
df = df.drop('ID', 1)   

#split into input and output columns
X, y = df.iloc[:, :-1], df.iloc[:, -1]


#load the model
model2 = xgb.XGBClassifier()
model2.load_model("../wilsongenai_xg_boost_model.txt")
preds = model2.predict(X)

#save the predictions
np.savetxt("predictions_xgboost", preds)
