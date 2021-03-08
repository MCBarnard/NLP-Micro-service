from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from nlp.lib.training import ModelTrainer
from nlp.lib.question import AskQuestion
import random
import json
import pickle
import numpy as np
import os

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

class SystemUp(APIView):
    def get(self, request):
        answer = {
            'code': 200,
            'response': 'HTTP OK'
        }
        return Response(answer)

class AnswerQuestion(APIView):
    def post(self, request):
        question = request.POST['question']
        neuralAnswer = AskQuestion.ask(self, question)
        answer = {
            'code': 200,
            'question': question,
            'answer': neuralAnswer
        }
        return Response(answer)