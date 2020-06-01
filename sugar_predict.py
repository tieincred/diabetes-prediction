# -*- coding: utf-8 -*-
"""SUGAR PREDICT

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JIxDKWa4HWGND4hSJNWl38O8mtVKKujc
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import tensorflow as tf

sess = tf.InteractiveSession()

import numpy as np

import pandas as pd

from google.colab import files
uploaded = files.upload()

import io
df2 = pd.read_csv(io.BytesIO(uploaded['diabetes.csv']))

df2

df2.columns

cols_to_norm = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
       'BMI', 'DiabetesPedigreeFunction']

df2[cols_to_norm] = df2[cols_to_norm].apply(lambda x: (x - x.min())/(x.max()-x.min()))

df2.head()

df2.columns

num_preg = tf.feature_column.numeric_column('Pregnancies')
plasma_gluc = tf.feature_column.numeric_column('Glucose')
dias_press = tf.feature_column.numeric_column('BloodPressure')
tricep = tf.feature_column.numeric_column('SkinThickness')
insulin = tf.feature_column.numeric_column('Insulin')
bmi = tf.feature_column.numeric_column('BMI')
Pedigree = tf.feature_column.numeric_column('DiabetesPedigreeFunction')
age = tf.feature_column.numeric_column('Age')

df2.shape

import random

li = ['A' ,'B' , 'C', 'D']

a_list = []

for i in range(768):
  a_list.append(random.choice(li))

df = pd.DataFrame(a_list)

df.head()

df = df.rename(columns={"0": "Class"})

df

frames = [df2,df]

diabetes = pd.concat(frames, axis =1)

diabetes

diabetes.rename(columns={0:'class'},inplace=True)

diabetes

assigend_group = tf.feature_column.categorical_column_with_vocabulary_list('class',['A','B','C','D'])

diabetes['Age'].hist(bins=20)

age_bucket = tf.feature_column.bucketized_column(age,boundaries=[20,30,40,50,60,70,80])

feat_cols = [num_preg, plasma_gluc,dias_press,tricep,insulin,bmi,Pedigree,age_bucket ]

k_data = diabetes.drop('Outcome',axis = 1)

labels = diabetes['Outcome']

from sklearn.model_selection import train_test_split

x_train, x_eval, y_train, y_eval = train_test_split(k_data,labels,test_size=0.3, random_state = 101)

input_func = tf.estimator.inputs.pandas_input_fn(x=x_train,y=y_train,batch_size=10,num_epochs=1000,shuffle=True)

model = tf.estimator.LinearClassifier(feature_columns=feat_cols,n_classes=2)

model.train(input_fn=input_func,steps=1000)

eval_input_func = tf.estimator.inputs.pandas_input_fn(x=x_eval,y=y_eval,batch_size=10,num_epochs=1,shuffle=False)

results = model.evaluate(eval_input_func)

results

pred_input_func = tf.estimator.inputs.pandas_input_fn(x=x_eval,batch_size=10,num_epochs=1,shuffle=False)

prediction = model.predict(pred_input_func)

my_pred = list(prediction)

my_pred

dnn_model = tf.estimator.DNNClassifier(hidden_units=[10,10,10],feature_columns=feat_cols,n_classes=2)

embedded_group_col = tf.feature_column.embedding_column(assigend_group,dimension=4)

feat_cols = [num_preg, plasma_gluc,dias_press,tricep,insulin,bmi,Pedigree,age_bucket,embedded_group_col ]

input_func = tf.estimator.inputs.pandas_input_fn(x=x_train,y=y_train,batch_size=10,num_epochs=1000,shuffle=True)

dnn_model = tf.estimator.DNNClassifier(hidden_units=[10,10,10],feature_columns=feat_cols,n_classes=2)

dnn_model.train(input_fn =input_func,steps=1000 )

eval_input_func = tf.estimator.inputs.pandas_input_fn(x=x_eval,y=y_eval,batch_size=10,num_epochs=1,shuffle=False)

results = dnn_model.evaluate(eval_input_func)

results