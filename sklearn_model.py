#!/usr/bin/python

# CSV Structure
# actor_score, length, Genre * 28, mpaa * 4, imdb_rating
# actor_score = atan(Sum(log10(100000/ranking)))
# length in minutes
# genre index: Comedy Short Animation Drama History War Horror Sci-Fi Biography Documentary Family News Action Romance Musical Fantasy Adventure Mystery Thriller Music Crime Sport Western Adult Film-Noir Talk-Show Reality-TV Game-Show
# mpaa index: 0-13 13-17 17-20 20-150

import sklearn.neural_network as net
import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import pandas as pd
from sklearn.model_selection import train_test_split

rawdata = pd.read_csv('outo.csv', header = None)
paras = rawdata.ix[:,:33].copy()
# print paras.head()
ratings = rawdata.ix[:,34].copy()
# print ratings.head()

paras_train, paras_test, ratings_train, ratings_test = train_test_split(paras, ratings, test_size = 0.2)

model = net.MLPRegressor(hidden_layer_sizes=(100, ), activation='tanh', solver='adam',  learning_rate='constant', learning_rate_init=0.001, max_iter = 10)
scores = []
for i in range(50):
    model.partial_fit(paras_train, ratings_train)
    # predictions = model.predict(paras_test)
    scores.append(model.score(paras_test, ratings_test))

# model.fit(paras_train, ratings_train)
# print predictions[0:10]
# print ratings_test.values[0:10]
# print scores
plt.plot(scores)
plt.ylabel('Score of Prediction')
plt.xlabel('Number of trainings (each training contains 10 iterations)')
plt.show()

# # print model.coefs_[1]
# w = model.coefs_[0]
# x = range(len(w[0]))
# y = range(len(w))
# X, Y = np.meshgrid(x,y)
# fig = plt.figure()
# # ax = fig.gca(projection = '3d')
# plt.scatter(X,Y, marker = 's', c = w, cmap = cm.jet, s = 60, linewidth = 0.1)
# plt.colorbar()
# plt.xlabel('Indices of neurons in hidden layer')
# plt.ylabel('Indices of features')
# plt.show()
