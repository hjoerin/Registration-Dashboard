from django.db import models
import pandas as pd
import os

# Create your models here.
n_data=pd.read_csv('unitedndf.csv')
print(n_data)

n_intercept1 = 118.7846329
h_coef = 0.08179365
r_coef = 0.71299317
s5_coef = 1.2995183


''' FIX
def pred_nHRS(H, R, S5):
  #This function performs a multiple regression using historical data from the dataframe
  #to develop a model for the number of FTIACs that will be attending GVSU in the fall.
  #It takes the most recent data values obtained for housing, registration and session 5 
  #orientation numbers as input parameters and calculates the predicted number of FTIACs 
  #to attend in the fall using the model.
  HRSx = df_N[['Housing', 'Reservations', 'S5']]
  HRSy = df_N['FTIACs']
  n_model = LinearRegression().fit(HRSx, HRSy)
  HRSpred = n_model.predict(HRSx)
  coefs = n_model.coef_
  n = H*coefs[0] + R*coefs[1] + S5*coefs[2] + n_model.intercept_ #Calculates the new value of n using the previous model and input parameters

  return n #returns the predicted value for n
print(n)



'''
