#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:55:35 2022

@author: aastha
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from pytorch_tabnet.tab_model import TabNetClassifier
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_recall_curve, roc_curve, roc_auc_score, matthews_corrcoef 
import seaborn as sns
from pandas import read_csv
from sklearn.impute import SimpleImputer


#load all data
data = read_csv('pipeline.csv')
df = data.copy()
df = df.drop('ID', 1)

#collect header to display missing values further down in the code
header = list(df.columns)
header.remove('Outcome')

#declare columns as categorical or numeric etc
for col in ['Function', 'LoF_HC_Canonical', 'Pfam_imp_domain', 'Outcome']:
    df[col] = df[col].astype('category')

#constant imputer
constant_imputer = SimpleImputer(strategy='constant',fill_value=-99)
df = constant_imputer.fit_transform(df)


#split into input and output columns
X, y = df[:, :-1], df[:, -1]


#split the dataset
x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=0.30, random_state=8)
x_val, x_test, y_val, y_test = train_test_split(x_val, y_val, test_size=0.50, random_state=8)

print("X train shape: ", x_train.shape)
print("X validation shape: ", x_val.shape)
print("X test shape: ", x_test.shape)
print("Y train shape: ", y_train.shape)
print("Y validation shape: ", y_val.shape)
print("Y test shape: ", y_test.shape)


# define the model
clf = TabNetClassifier(optimizer_fn=torch.optim.Adam,
                       optimizer_params=dict(lr=2e-2),
                       scheduler_params={"step_size": 10,  
                                         "gamma": 0.90},
                       scheduler_fn=torch.optim.lr_scheduler.StepLR,
                       mask_type='entmax' 
                      )

# fit the model
clf.fit(
    x_train, y_train,
    eval_set=[(x_train, y_train), (x_val, y_val)],
    eval_name=['train', 'valid'],
    eval_metric=['auc', 'accuracy'],
    max_epochs=1000, patience=100,
    batch_size=72, virtual_batch_size=36,
    num_workers=0,
    weights=1,
    drop_last=False
)

#plot feature importance
fig0 = plt.figure()
y_pred = clf.predict(x_test)
clf.feature_importances_
feat_importances = pd.Series(clf.feature_importances_, index=header)
feat_importances.nlargest(20).plot(kind='barh')
plt.title('Feature Importance')
plt.ylabel('Feature')
plt.xlabel('Score')
plt.savefig("feature_importance.png", dpi=600, bbox_inches='tight')


# plot losses
fig1 = plt.figure()
plt.plot(clf.history['loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
#plt.legend(['Train', 'Val'], loc = 'upper right')
plt.savefig("loss.png", dpi=600)
    

# plot accuracy
fig2 = plt.figure()
plt.plot(clf.history['train_accuracy'])
plt.plot(clf.history['valid_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='lower right') 
plt.savefig("accuracy.png", dpi=600)
    

# plot auc
fig3 = plt.figure()
y_pred_proba = clf.predict_proba(x_test)[:,1]
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


# plot learning rates
fig4 = plt.figure()
plt.plot(clf.history['lr'])
plt.title('Model Learning Rate')
plt.ylabel('Learning Rate')
plt.xlabel('Epoch')
plt.savefig("learning_rate.png", dpi=600)
    

# determine best accuracy for test set
preds = clf.predict(x_test)
test_acc = accuracy_score(preds, y_test)


# determine best accuracy for validation set
preds_valid = clf.predict(x_val)
valid_acc = accuracy_score(preds_valid, y_val)

#determine matthews correlation coefficient
MCC = matthews_corrcoef(y_test, preds)


print(f"BEST ACCURACY SCORE ON VALIDATION SET : {valid_acc}")
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


#Finally, save the model
clf.save_model("tabnet.model")

