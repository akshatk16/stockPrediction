# predict stock prices using ML

# import dependencies
import quandl
import numpy as np
from math import ceil, floor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import matplotlib.pyplot as plt

# get stock data
quandl.ApiConfig.api_key = "QxjBQqyAsBTrnpSkZqwc"

# The WIKIP API was discotinued in 2018 and hence further data is not available
df = quandl.get("WIKI/AAPL")
print(df.head())

# get only 'adjusted close'
df = df[['Adj. Close']]
print(df.head())

# how many days in future to predict(n)
predict_for_days = 15

# New column for dependent variables shifted n units up
df['Prediction'] = df[['Adj. Close']].shift(-predict_for_days)
print(df.tail())

# independent data set (X)
X = np.array(df.drop(['Prediction'], 1))
# Remove last n rows
X = X[:-predict_for_days]
print(X)

# dependent data set (y)
y = np.array(df['Prediction'])
y = y[:-predict_for_days]
print(y)

# Split into train/test
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train using Supprot Vector Regressor
svr_rbf = SVR('rbf', gamma=0.1, C=1000)
svr_rbf.fit(x_train, y_train)

# Test the svr model
svm_confidence = svr_rbf.score(x_test, y_test)
print(svm_confidence)

# Linear Regression model
lr = LinearRegression()
lr.fit(x_train, y_train)

# Test the lr model
lr_confidence = lr.score(x_test, y_test)
print(lr_confidence)

# last n rows from original dataset
x_predict = np.array(df.drop(['Prediction'], 1))[-predict_for_days:]
print(x_predict)

# predict for next n days using svm
svr_prediction = svr_rbf.predict(x_predict)
print('Using SVM: ', svr_prediction)

# predict for next n days using LR
lr_prediction = lr.predict(x_predict)
print('Using LR: ', lr_prediction)

# Plot next n days prediction
plt.plot(svr_prediction, color = 'blue', marker = '.', linestyle = '-.', label='Linear Regression')
plt.plot(lr_prediction, color = 'green', marker = 'x', linestyle = '--', label='Support Vector Regression')
plt.xticks(np.arange(predict_for_days), np.arange(1, predict_for_days+1))
minV = floor(min(min(lr_prediction), min(svr_prediction)))
maxV = ceil(max(max(lr_prediction)+1, max(svr_prediction)+1))
plt.yticks(np.arange(minV, maxV, floor((maxV-minV)/8)))
plt.ylabel('Predicted Price')
plt.xlabel('No. of days next')
plt.grid()
plt.legend()
plt.show()
plt.close()
