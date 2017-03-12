# -*- coding: utf-8 -*-

import sjkabc
import re
import os
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import numpy as np
import sys

melodies = []
for tune in sjkabc.parse_file("tunes2.abc"):    
    try:
        #Dメジャーの曲だけを使用する
        if tune.key == ['Dmaj']:
            melodies.append(re.findall(r"[_=\\^]?[a-gA-Gz][,']{0,3}", tune.expanded_abc))
    except:
            pass

chars = sorted(list(set(sum(melodies,[]))))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

maxlen = 10
step = 1
sentences = []
next_chars = []
for melody in melodies:
    for i in range(0, len(melody) - maxlen, step):
        sentences.append(melody[i: i + maxlen])
        next_chars.append(melody[i + maxlen])

print('nb sequences:', len(sentences))

print('Vectorization...')

X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(maxlen, len(chars))))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model.fit(X, y, batch_size=128, nb_epoch=1)

model.save_weights('param.hdf5')

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

#Dメジャーの曲なので、始まりの音はDにしている
start_sentence = ['D'] * 10

#民族音楽は順次進行の曲が多いので、diversityは0.5ぐらいがいい。
#大きくしすぎない方が良い。
diversity = 0.5

generated = ''
sentence = start_sentence[-10:]
print('----- Generating with seed: "' + str(sentence) + '"')

for i in range(400):
    x = np.zeros((1, maxlen, len(chars)))
    for t, char in enumerate(sentence):
        x[0, t, char_indices[char]] = 1.

    preds = model.predict(x, verbose=0)[0]
    next_index = sample(preds, diversity)
    next_char = indices_char[next_index]

    generated += next_char
    sentence.pop(0)
    sentence.append(next_char)

    sys.stdout.write(next_char)
    sys.stdout.flush()
