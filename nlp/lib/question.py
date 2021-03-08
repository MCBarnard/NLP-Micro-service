import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model
import os


class AskQuestion():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path_intents = os.path.join(module_dir, '../../intents.json')
    file_path_words = os.path.join(module_dir, '../NLPModel/words.pkl')
    file_path_classes = os.path.join(module_dir, '../NLPModel/classes.pkl')
    file_path_model = os.path.join(module_dir, '../NLPModel/chatbot_model.h5')

    lemmatizer = WordNetLemmatizer()
    intents = json.loads(open(file_path_intents).read())
    words = pickle.load(open(file_path_words, 'rb'))
    classes = pickle.load(open(file_path_classes, 'rb'))
    model = load_model(file_path_model)
    ERROR_THRESHOLD = 0.25

    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize((sentence))
        sentence_words = [AskQuestion.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(sentence):
        sentence_words = AskQuestion.clean_up_sentence(sentence)
        bag = [0] * len(AskQuestion.words)
        for w in sentence_words:
            for i, word in enumerate(AskQuestion.words):
                if word == w:
                    bag[i] = 1

        return np.array(bag)

    def predict_class(sentence):
        bagged_words = AskQuestion.bag_of_words(sentence)
        res = AskQuestion.model.predict(np.array([bagged_words]))[0]

        results = [[i, r] for i, r in enumerate(res) if r > AskQuestion.ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)

        return_list = []
        for r in results:
            return_list.append({
                'intent': AskQuestion.classes[r[0]],
                'probability': str(r[1])
            })
        return return_list

    def get_response(intents_list, intents_json):
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result

    def ask(self, question):
        message = question
        ints = AskQuestion.predict_class(message)
        response = AskQuestion.get_response(ints, AskQuestion.intents)
        return response
