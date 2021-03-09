# Natural Language Processing MS

## Licence
MIT

## About

The chatbot_nlp microservice uses intents.json to build a nearal network and give appropriate feedback.

To use this service for your own chatbot, simply edit `intents.json` adding a tag, some example patterns of the question you are expecting and then add the corresponding response

## Get it up and running

* Make sure you have all of the files required packages installed (RequiredPackages.md)
* Run `python manage.py runserver` to start a server on http://127.0.0.1:8000

## ENDPOINTS

`GET`: http://127.0.0.1:8000/

`{
    "code":200,
    "response":"HTTP OK"
}`

`POST`: http://127.0.0.1:8000/ask

`{
    "code": 200,
    "question": "Some Question",
    "answer": "Some Answer"
}`