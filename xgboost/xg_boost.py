#tutorial: https://machinelearningmastery.com/develop-first-xgboost-model-python-scikit-learn/
#https://www.datacamp.com/tutorial/xgboost-in-python
    
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from pandas import read_csv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_curve, roc_curve, roc_auc_score, matthews_corrcoef 
import seaborn as sns
from sklearn.impute import SimpleImputer
from numpy import nan


#load all data
data = read_csv('pipeline.csv')
df = data.copy()
df = df.drop('ID', 1)

#subset the daya into x and y
X, y = df.iloc[:,:-1],df.iloc[:,-1]

#split data into test and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

#instantiate an XGBoost classifier 
model = xgb.XGBClassifier(scale_pos_weight=3.95, base_score=0.5, booster='gbtree', callbacks=None,
              colsample_bylevel=1, colsample_bynode=1, colsample_bytree=0.9,
              early_stopping_rounds=None, enable_categorical=False,
              eval_metric=None, gamma=0.2, gpu_id=-1, grow_policy='depthwise',
              importance_type=None, interaction_constraints='',
              learning_rate=0.25, max_bin=256, max_cat_to_onehot=4,
              max_delta_step=0, max_depth=6, max_leaves=0, min_child_weight=1,
              missing=nan, monotone_constraints='()', n_estimators=50, n_jobs=0,
              num_parallel_tree=1, predictor='auto', random_state=0,
              reg_alpha=0, reg_lambda=1, seed=123)

#fit the model and make predictions
model.fit(X_train,y_train)
preds = model.predict(X_test)

#save the model
model.save_model("xg_boost_model.txt")


###CHECK MODEL PERFORMANCE
# plot auc
fig3 = plt.figure()
y_pred_proba = model.predict_proba(X_test)[:,1]
fpr, tpr, threshold = roc_curve(y_test,  y_pred_proba)
#Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores
roc_auc = roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr)
plt.title('ROC Curve')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.savefig("auc.png", dpi=600)


# plot precision recall curve
fig3_2 = plt.figure()
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
plt.plot(recall, precision)
plt.title('Precision-Recall Curve')
plt.ylabel('Precision')
plt.xlabel('Recall')
plt.savefig("prcurve.png", dpi=600)


# determine best accuracy for test set
preds = model.predict(X_test)
test_acc = accuracy_score(preds, y_test)

#determine matthews correlation coefficient
MCC = matthews_corrcoef(y_test, preds)

print(f"BEST ACCURACY SCORE ON TEST SET : {test_acc}")
print("AUC ROC : ", roc_auc)
print("MCC : ", MCC)

print(classification_report(y_test, preds))


#plot confusion matrix
fig5 = plt.figure()
sns.heatmap(confusion_matrix(y_test, preds), cmap = 'Blues', annot = True, fmt = 'd', linewidths = 5, cbar = False, annot_kws = {'fontsize': 15},
            yticklabels = ['Benign', 'Pathogenic'], xticklabels = ['Predicted Benign', 'Predicted Pathogenic'])
plt.title('Confusion Matrix')
plt.savefig("confusion_matrix.png", dpi=600)


#Visualize Boosting Trees and Feature Importance using plot_tree() function
#boosting trees
figure6 = plt.figure()
xgb.plot_tree(model,num_trees=0)
plt.rcParams['figure.figsize'] = [100, 200]
plt.savefig("boosted_trees.png", dpi=600)

#feature importance
figure7 = plt.figure()
xgb.plot_importance(model)
plt.rcParams['figure.figsize'] = [1, 3]
plt.margins()
plt.savefig("feature_importance.png", bbox_inches='tight')

