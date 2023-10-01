import json
import os
import random
import time

import dotenv
import openai
import requests
from django.template import loader
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BrainstormData, Quiz

# import backend.settings as settings

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


openai.api_key = os.environ["OPEN_AI_API_KEY"]





##################################################################################


def RedditAuth():

    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             data={'grant_type': 'password', 'username': os.environ["REDDIT_USERNAME"], 'password': os.environ["REDDIT_PASSWORD"]},
                             auth=requests.auth.HTTPBasicAuth(os.environ["REDDIT_CLIENTID"], os.environ["REDDIT_CLIENTSECRET"])).json()

    return (response)


##################################################################################

class Learn(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        all_data = BrainstormData.objects.all()
        return Response(data={"data":[{"query":x.query} for x in all_data]})

##################################################################################


class Brainstorm(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        query = request.GET.get("query")

        brainstorm_query_set = BrainstormData.objects.filter(query=query)
        if brainstorm_query_set.exists():
            brainstormRawData = brainstorm_query_set.last().data
        else:

            ################################################################
            # Google

            # Youtube

            ytLink = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&topicId=/m/01k8wb&q={}".format(
                query.replace(" ", "%20"))
            ytData = eval(requests.get(ytLink, headers={
                "Authorization": "Bearer " + os.environ["YOUTUBE_ACCOUNT"]}).text.replace("true", "True").replace("false", "False"))

            if "error" in ytData.keys():
                response = eval(requests.post('https://oauth2.googleapis.com/token', data={
                                'client_id': os.environ["YOUTUBE_CLIENTID"], 'client_secret': os.environ["YOUTUBE_CLIENTSECRET"], 'refresh_token': os.environ["YOUTUBE_REFRESH"], 'grant_type': 'refresh_token'}).text)
                print(response)
                os.environ["YOUTUBE_ACCOUNT"] = response['access_token']
                dotenv.set_key(dotenv_file, "YOUTUBE_ACCOUNT",
                               os.environ["YOUTUBE_ACCOUNT"])
                ytData = eval(requests.get(ytLink, headers={
                    "Authorization": "Bearer " + os.environ["YOUTUBE_ACCOUNT"]}).text.replace("true", "True").replace("false", "False"))

            # Reddit

            def RedditData():
                redditLink = f'https://oauth.reddit.com/r/SBU/search?q=education OR learning OR tutorial {query}'
                redditData = requests.get(redditLink, headers={
                    'Authorization': f'bearer {os.environ["REDDIT_ACCOUNT"]}',
                    'User-agent': 'Mozilla/5.0',
                }, params={'limit': '5'}).json()
                return redditData

            try:
                redditData = RedditData()
            except Exception as e:
                # print(str(e).title())
                while True:
                    print("ERROR IN REDDIT.")
                    reddit_auth_data = RedditAuth()
                    if "error" not in reddit_auth_data.keys():
                        os.environ["REDDIT_ACCOUNT"] = reddit_auth_data['access_token']
                        dotenv.set_key(dotenv_file, "REDDIT_ACCOUNT",
                                       os.environ["REDDIT_ACCOUNT"])
                        break
                redditData = RedditData()

            # Github

            ghLink = "https://api.github.com/search/topics?per_page=10&q={}".format(
                query.replace(" ", "%20"))
            ghData = requests.get(ghLink).json()

            # Wikipedia

            wpLink = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={query.replace(' ', '%20')}"
            wpData = requests.get(wpLink).json()
            wpData = {"items": [{"title": item, "link": wpData[3][k]}
                                for k, item in enumerate(wpData[1])]}

            # Join All
            brainstormRawData = {
                "success": "true",
                "message": "Working.",
                "data": {
                    "google": [],
                    "youtube": ytData,
                    "reddit": redditData,
                    "github": ghData,
                    "wikipedia": wpData
                }}

            BrainstormData.objects.create(query=query, data=brainstormRawData)
            ####################################################
        # time.sleep(3)
        return Response(data=brainstormRawData)

##################################################################################

class Practice(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        all_data = Quiz.objects.all()
        return Response(data={"data":[{"query":x.query} for x in all_data]})

##################################################################################

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

            quizRawData = completion.choices[0].message['content'].replace("\"", '"').replace("\n", "").replace(
                "choices", "options").replace("answer", "correctAnswer").replace("correct_answer", "correctAnswer")
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
            "quiz": quizRawData
        })
