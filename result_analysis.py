#!/usr/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

w0 = pd.read_csv('w0.csv', header = None)
w1 = pd.read_csv('w1.csv', header = None)
# Data structure in w0
# actor score(0), length(1), genre(2-29), mpaa rating(30-33)
# Data in w1: weight for each neuron in hidden layer

# neuron_norm = [pow(w0.ix[i,:],2).sum() for i in range(100)]
# actor_norm = [pow(w0.ix[i,0],2).sum() for i in range(100)]
# length_norm = [pow(w0.ix[i,1],2).sum() for i in range(100)]
# genre_norm = [pow(w0.ix[i,2:29],2).sum() for i in range(100)]
# mpaa_norm = [pow(w0.ix[i,30:33],2).sum() for i in range(100)]

neuron_norm = [pow(w0.ix[i,:],2).sum() * w1.values[i] for i in range(100)]
actor_norm = [pow(w0.ix[i,0],2).sum() * w1.values[i] for i in range(100)]
length_norm = [pow(w0.ix[i,1],2).sum() * w1.values[i] for i in range(100)]
genre_norm = [pow(w0.ix[i,2:29],2).sum() * w1.values[i] for i in range(100)]
mpaa_norm = [pow(w0.ix[i,30:33],2).sum() * w1.values[i] for i in range(100)]

neuron_norm = sum(neuron_norm)
actor_norm = sum(actor_norm)
length_norm = sum(length_norm)
genre_norm = sum(genre_norm)
mpaa_norm = sum(mpaa_norm)

# plt.plot(range(100), neuron_norm, label = 'Total norm')
# plt.plot(range(100), actor_norm, label = 'Actor norm')
# plt.plot(range(100), length_norm, label = 'Length norm')
# plt.plot(range(100), genre_norm, label = 'Genre norm')
# plt.plot(range(100), mpaa_norm, label = 'Mpaa norm')
# plt.legend()

explode = (0.05, 0.05, 0.1, 0.05)
sizes = [abs(actor_norm), abs(length_norm), abs(genre_norm), abs(mpaa_norm)]
plt.figure(0, figsize=(8,7), dpi = 80)
plt.pie(sizes, labels = ['actor_norm', 'length_norm', 'genre_norm', 'mpaa_norm'],explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
plt.legend(loc = 3)
plt.savefig('relations_origin.png')

explode = (0.1, 0.05, 0.05, 0.05)
sizes_per = [abs(actor_norm), abs(length_norm), abs(genre_norm)/28, abs(mpaa_norm)/4]
plt.figure(1, figsize=(8,7), dpi = 80)
plt.pie(sizes_per, labels = ['actor_norm', 'length_norm', 'genre_norm', 'mpaa_norm'],explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
plt.legend(loc = 2)
plt.savefig('relations_normalized.png')
plt.show()
