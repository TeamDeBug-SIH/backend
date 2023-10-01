import json
import random

import openai
import requests
from django.template import loader
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
import backend.settings as settings
from authentication.models import User
from .models import Quiz, TopicData

openai.api_key = settings.OPEN_AI_API_KEY
from django.contrib.auth import authenticate, login

from googlesearch import search

search_engines = {
    "Google": "",
    "startpage": "",
    "GitHub": "site:github.com",
    "Reddit": "site:reddit.com *learn",
    "Wikipedia": "site:https://en.wikipedia.org/wiki",
}


def Search(query, site_query="", num_results=10):
    query = f"{query} {site_query}".strip()
    search_results = list(search(query, num=num_results, verify_ssl=True, pause=2))
    return search_results


def SearchStart(query, site_query="", num_results=10):
    query = f"{query} {site_query}".strip()
    from startpage import Startpage

    task = Startpage()
    search_results = list(task.search(query))
    return search_results

def search_api(data):
    query = data.get("query", "python")  # Default query
    selected_engine = data.get("engine", "Google")  # Default search engine

    site_query = search_engines.get(selected_engine, "")
    num_results = data.get("num_results", 10)
    search_results = SearchStart(query, site_query, num_results=num_results)

    # Convert the search results to a JSON response
    response = [{"title": result, "url": result} for result in search_results]
    return response


class Learn(APIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = ()

    def get(self, request):
        query = request.GET.get("query")
        engine = request.GET.get("engine")

        topic_data = TopicData.objects.filter(topic=query)
        if topic_data.exists():
            google_data = topic_data.Googledata if engine == "google" else []
            # reddit_data = topic_data.Redditdata if engine == "reddit" else []
            # yt_data = topic_data.Ytdata if engine == "youtube" else []
        else:
            topic_data = TopicData.objects.create(topic=query)

        ##################################################### Google
        if google_data:
            g = google_data
        else:
            g = search_api(
                {"query": f"{query}", "engine": f"{engine}", "num_results": 5}
            )
            TopicData.objects.create(topic=query)

        ytLink = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={}".format(query.replace(" ","%20"))
        ytData = eval(requests.get(ytLink, headers = {"Authorization": "Bearer " + settings.YOUTUBE_ACCOUNT}).text.replace("true","True").replace("false","False"))

        #################################################### Reddit

        redditLink = f'https://oauth.reddit.com/r/SBU/search?q={query}'
        redditData = requests.get(redditLink, headers={
            'Authorization': f'bearer {settings.REDDIT_ACCOUNT}',
            'User-agent': 'Mozilla/5.0',
            },params={'limit':'5'}).json()

        ####################################################

        return Response(
            data={
                "success": "true",
                "message": "Working.",
                "data": {
                    "t": query,
                    "google": [g],
                    "youtube":ytData,
                    "reddit":redditData,
                    "github": [],
                    "wikipedia": [],
                },
            }
        )


class QuizView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = ()

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
                    {
                        "role": "user",
                        "content": f"generate a quiz with mcqs about {query} with 10 questions in json",
                    }
                ],
            )

            quizRawData = (
                completion.choices[0]
                .message["content"]
                .replace('"', '"')
                .replace("\n", "")
            )
            if "```json" in quizRawData:
                quizRawData = quizRawData.split("```json")[1]
            quizRawData = json.loads(quizRawData)
            Quiz.objects.create(query=query, data=quizRawData)

        # sampleData = {
        #     "role": "assistant",
        #     "content": "Sure! Here's an example of a Python quiz with two questions in JSON format:\n\n```json\n{\n  \"quiz\": {\n    \"title\": \"Python Quiz\",\n    \"questions\": [\n      {\n        \"question\": \"What is the output of the following code?\\n\\nx = [1, 2, 3, 4, 5]\\nprint(x[1:3])\",\n        \"options\": [\n          \"1\",\n          \"[1, 2]\",\n          \"[2, 3]\",\n          \"[2, 3, 4]\"\n        ],\n        \"answer\": \"[2, 3]\"\n      },\n      {\n        \"question\": \"Which of the following statements is true?\\n\\na) Python is a high-level programming language.\\nb) Python is an interpreted language.\\nc) Python is an object-oriented language.\\nd) All of the above.\",\n        \"options\": [\n          \"a) Python is a high-level programming language.\",\n          \"b) Python is an interpreted language.\",\n          \"c) Python is an object-oriented language.\",\n          \"d) All of the above.\"\n        ],\n        \"answer\": \"d) All of the above.\"\n      }\n    ]\n  }\n}\n```\n\nFeel free to modify the questions, options, and answers as per your requirement."
        # }
        # sampleData['content'].split("```json")[1]

        return Response(
            data={"success": "true", "message": "Working.", "quiz": quizRawData}
        )
