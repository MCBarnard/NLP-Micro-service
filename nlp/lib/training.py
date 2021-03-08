import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import os


class ModelTrainer():

    def clear_model():
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path_words = os.path.join(module_dir, '../NLPModel/words.pkl')
        file_path_classes = os.path.join(module_dir, '../NLPModel/classes.pkl')
        file_path_model = os.path.join(module_dir, '../NLPModel/chatbot_model.h5')
        os.remove(file_path_words)
        os.remove(file_path_classes)
        os.remove(file_path_model)

    def train():
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, '../../intents.json')
        lemmatizer = WordNetLemmatizer()

        intents = json.loads(open(file_path).read())

        words = []
        classes = []
        documents = []
        ignore_letters = ['?', '!', '.', ',']

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                word_list = nltk.word_tokenize(pattern)
                words.extend(word_list)
                documents.append((word_list, intent['tag']))
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        # Split words into single words
        words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
        # Remove duplicate words
        words = sorted(set(words))
        classes = sorted(set(classes))
        # Save list into files
        pickle.dump(words, open(module_dir + '/../NLPModel/words.pkl', 'wb'))
        pickle.dump(classes, open(module_dir + '/../NLPModel/classes.pkl', 'wb'))

        # Assign values to words
        training = []
        output_empty = [0] * len(classes)

        for document in documents:
            bag = []
            word_patterns = document[0]
            word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(document[1])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save(module_dir + '/../NLPModel/chatbot_model.h5', hist)
        print('Successfully built the model')
        return True
