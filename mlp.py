from keras.models import Sequential,Graph
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import pandas as pd
import time,math
import matplotlib.pyplot as plt
from Confuse import main

X = pd.read_csv('Train/Train_Combine.csv', usecols=[
                'T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM'])
Y = pd.read_csv('Train/Train_Combine.csv', usecols=['PM 2.5'])

X = X.values
Y = Y.values

X2 = pd.read_csv('Test/Test_Combine.csv', usecols=[
                 'T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM'])
Y2 = pd.read_csv('Test/Test_Combine.csv', usecols=['PM 2.5'])

X2 = X2.values
Y2 = Y2.values

model = Sequential()

model.add(Dense(10, input_dim=8, init='uniform'))
model.add(Activation('tanh'))
model.add(Dense(10,input_dim=10, init='uniform'))
model.add(Activation('tanh'))
model.add(Dense(1,input_dim=10, init='uniform'))
model.add(Activation('tanh'))

sgd = SGD(lr=0.1, decay=1e-3, momentum=0.5, nesterov=True)
model.compile(loss='mse',optimizer=sgd)

model.fit(X, Y,nb_epoch=20,batch_size=1,show_accuracy=False)
score = model.evaluate(X2, Y2, batch_size=1)
preds = model.predict(X2, batch_size=1, verbose=0)


main(preds,Y2)

plt.plot(xrange(0, 441), preds, label='Observed')
plt.plot(xrange(0, 441), Y2, label='Expected')
plt.xlabel('Data Points')
plt.ylabel('PM 2.5')
plt.legend(loc='upper right')
plt.show()

print "Error: ",score