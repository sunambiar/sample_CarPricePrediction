#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 12:45:15 2021

@author: sureshnambiar
"""


from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
import datetime

currYear = datetime.datetime.now().year 
 
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/', methods=['GET'])
def Home():
  return render_template('index.html')

standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])
def predict():
  Fuel_Type_Diesel = 0
  if request.method == 'POST':
    YearVal = int(request.form['Year'])
    Present_Price = float(request.form['Present_Price'])
    Kms_Driven = int(request.form['Kms_Driven'])
    Owner = int(request.form['Owner'])
    Fuel_Type_Petrol_Descr = request.form['Fuel_Type_Petrol']
    Fuel_Type_Petrol = 0
    Fuel_Type_Diesel = 0
    if (Fuel_Type_Petrol_Descr == 'Petrol'):
      Fuel_Type_Petrol = 1
    elif (Fuel_Type_Petrol_Descr == 'Diesel'):
      Fuel_Type_Diesel = 1 
    Year = currYear - YearVal
    #--- understood that if both are zeros, it is CNG only
    Seller_Type_Individual = request.form['Seller_Type_Individual']
    if (Seller_Type_Individual == 'Individual'):
      Seller_Type_Individual = 1
    else:
      Seller_Type_Individual = 0
    Transmission_Manual = request.form['Transmission_Manual']
    if (Transmission_Manual == 'Manual'):
      Transmission_Manual = 1
    else:
      Transmission_Manual = 0
    prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, 
                  Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual,
                  Transmission_Manual]])
    output = round(prediction[0], 2)
    if output < 0:
      return render_template('index.html', prediction_texts='Sorry you cannot sell this car')
    else:
      return render_template('index.html', prediction_text='You can sell this Car at {} Lakhs.'.format(output))
  else:
    return render_template('index.html') 


if __name__ == '__main__':
  app.run(debug=True)


