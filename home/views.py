import json
import os
import random

import dotenv
import openai
import requests
from django.template import loader
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Quiz

# import backend.settings as settings


openai.api_key = os.environ["OPEN_AI_API_KEY"]


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class Learn(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        query = request.GET.get("query")
        ##################################################### Google

        

        ##################################################### Youtube

        ytLink = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=7&topicId=/m/01k8wb&q={}".format(query.replace(" ","%20"))
        ytData = eval(requests.get(ytLink, headers = {"Authorization": "Bearer " + os.environ["YOUTUBE_ACCOUNT"]}).text.replace("true","True").replace("false","False"))

        if "error" in ytData.keys():
            response = eval(requests.post('https://oauth2.googleapis.com/token', data={'client_id': os.environ["YOUTUBE_CLIENTID"],'client_secret': os.environ["YOUTUBE_CLIENTSECRET"],'refresh_token': os.environ["YOUTUBE_REFRESH"],'grant_type': 'refresh_token'}).text)
            os.environ["YOUTUBE_ACCOUNT"] = response['access_token']
            dotenv.set_key(dotenv_file, "YOUTUBE_ACCOUNT", os.environ["YOUTUBE_ACCOUNT"])
            ytData = eval(requests.get(ytLink, headers = {"Authorization": "Bearer " + os.environ["YOUTUBE_ACCOUNT"]}).text.replace("true","True").replace("false","False"))
        
        #################################################### Reddit

        redditLink = f'https://oauth.reddit.com/r/SBU/search?q={query}'
        redditData = requests.get(redditLink, headers={
            'Authorization': f'bearer {os.environ["REDDIT_ACCOUNT"]}',
            'User-agent': 'Mozilla/5.0',
            },params={'limit':'5'}).json()

        #################################################### 


        
        return Response(data={
            "success": "true", 
            "message": "Working.", 
            "data": {
                "google":[],
                "youtube":ytData,
                "reddit":redditData,
                "github":[],
                "wikipedia":[]
            }})
    

class QuizView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        query = request.GET.get("query")
        # generateNew =  request.GET.get("generateNew")

        quizes_query_set = Quiz.objects.filter(query=query)
        if quizes_query_set.exists():
            quizRawData = quizes_query_set.last().data
        
        else:
            # if generateNew == "true":
            #     print("Generated")
                
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"generate a quiz with mcqs about {query} with 10 questions in json"}
            ]
            )

            quizRawData = completion.choices[0].message['content'].replace("\"",'"').replace("\n","").replace("choices","options").replace("answer","correctAnswer").replace("correct_answer","correctAnswer")
            if "```json" in quizRawData:
                quizRawData = quizRawData.split("```json")[1]
            quizRawData = json.loads(quizRawData)
            Quiz.objects.create(query=query, data=quizRawData)


        # sampleData = {
        #     "role": "assistant",
        #     "content": "Sure! Here's an example of a Python quiz with two questions in JSON format:\n\n```json\n{\n  \"quiz\": {\n    \"title\": \"Python Quiz\",\n    \"questions\": [\n      {\n        \"question\": \"What is the output of the following code?\\n\\nx = [1, 2, 3, 4, 5]\\nprint(x[1:3])\",\n        \"options\": [\n          \"1\",\n          \"[1, 2]\",\n          \"[2, 3]\",\n          \"[2, 3, 4]\"\n        ],\n        \"answer\": \"[2, 3]\"\n      },\n      {\n        \"question\": \"Which of the following statements is true?\\n\\na) Python is a high-level programming language.\\nb) Python is an interpreted language.\\nc) Python is an object-oriented language.\\nd) All of the above.\",\n        \"options\": [\n          \"a) Python is a high-level programming language.\",\n          \"b) Python is an interpreted language.\",\n          \"c) Python is an object-oriented language.\",\n          \"d) All of the above.\"\n        ],\n        \"answer\": \"d) All of the above.\"\n      }\n    ]\n  }\n}\n```\n\nFeel free to modify the questions, options, and answers as per your requirement."
        # }
        # sampleData['content'].split("```json")[1]

        return Response(data={
            "success": "true", 
            "message": "Working.",
            "quiz":quizRawData
            })