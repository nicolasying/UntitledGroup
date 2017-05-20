#!/usr/bin/python
import sklearn.neural_network as net
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
from sklearn.model_selection import train_test_split
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
from matplotlib import gridspec

# Import raw data
rawdata = pd.read_csv('outo.csv', header = None)
# Seperate imdb ratings with other parameters
paras = rawdata.ix[:,:33].copy()
ratings = rawdata.ix[:,34].copy()
# Apply train_test_split to generate train and test data
paras_train, paras_test, ratings_train, ratings_test = train_test_split(paras, ratings, test_size = 0.2, random_state = 0)
# Model initialization:
trial_iter = 10
model = net.MLPRegressor(hidden_layer_sizes=(100, ), activation='tanh', solver='adam',  learning_rate='constant', learning_rate_init=0.001, max_iter = trial_iter)
scores = [] # Score for evaluating the precision of prediction
# Visulization of weights in network model.coefs_[]
w = np.zeros([34, 100])
x = range(1, len(w[0]) + 1)
y = range(1, len(w) + 1)
X, Y = np.meshgrid(x,y)
img = plt.figure(1, figsize = (15,4.5), dpi = 80, facecolor = (1,1,1))
gs = gridspec.GridSpec(1, 2, width_ratios = [3, 1])
plt.subplot(gs[0])
plt.imshow(w, cmap = cm.jet, vmin = -1, vmax= 1)
plt.xlabel('Indices of neurons in hidden layer')
plt.ylabel('Indices of features')
plt.colorbar()
# Score curve
plt.subplot(gs[1])
plt.plot(range(1,len(scores) + 1), scores, 'r', linewidth = 3)
plt.grid(True)
plt.xlim(0,201)
plt.ylim(0.17,0.21)
plt.ylabel('Score of Prediction')
plt.xlabel('Number of trainings (each training contains ' + str(trial_iter) + ' iterations)')
def make_frame(t):
    model.partial_fit(paras_train, ratings_train)
    # predictions = model.predict(paras_test)
    scores.append(model.score(paras_test, ratings_test))
    plt.clf()
    w = np.array(model.coefs_[0])
    plt.subplot(gs[0])
    plt.imshow(w, cmap = cm.jet, vmin = -1, vmax = 1)
    plt.xlabel('Indices of neurons in hidden layer')
    plt.ylabel('Indices of features')
    plt.colorbar()
    # Score curve
    plt.subplot(gs[1])
    plt.plot(range(1,len(scores) + 1), scores, 'r', linewidth = 3)
    plt.grid(True)
    plt.xlim(0,201)
    plt.ylim(0.17,0.21)
    plt.ylabel('Score of Prediction')
    plt.xlabel('Number of trainings (each training contains ' + str(trial_iter) + ' iterations)')
    return mplfig_to_npimage(img)


animation = VideoClip(make_frame, duration=10) # 5-second clip
animation.write_videofile("my_animation.mp4", fps=20) # export as video
# animation.write_gif("my_animation.gif", fps=20) # export as GIF

w0 = model.coefs_[0]
w1 = model.coefs_[1]

w0 = pd.DataFrame(w0)
w0.to_csv('w0.csv', header = None, index = None)
w1 = pd.DataFrame(w1)
w1.to_csv('w1.csv', header = None, index = None)

# for i in range(trials):
#     model.partial_fit(paras_train, ratings_train)
#     # predictions = model.predict(paras_test)
#     scores.append(model.score(paras_test, ratings_test))
#     imgs.append(draw_weight(model, filename = 'w-' + str(i + 1) + '.png', index = i + 1))

# Results visulization
# plt.figure(0)
# plt.plot(range(1, trials + 1), scores)
# plt.ylabel('Score of Prediction')
# plt.xlabel('Number of trainings (each training contains ' + str(trial_iter) + ' iterations)')
# plt.savefig('figure.png')
# # plt.show()
# plt.close(0)

# model.fit(paras_train, ratings_train)
# scores = model.score(paras_test, ratings_test)
# predictions = model.predict(paras_test)
# print predictions[0:10]
# print ratings_test.values[0:10]
# print scores

# # Visulization of weights in network model.coefs_[1]
# w = model.coefs_[0]
# x = range(1, len(w[0]) + 1)
# y = range(1, len(w) + 1)
# X, Y = np.meshgrid(x,y)
# plt.figure(figsize = (10,6), dpi = 80)
# plt.scatter(X,Y, marker = 's', c = w, cmap = cm.jet, s = 60, linewidth = 0.1)
# plt.colorbar()
# plt.xlabel('Indices of neurons in hidden layer')
# plt.ylabel('Indices of features')
# plt.savefig('w.png')
# plt.close()
