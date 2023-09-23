# from flask import Flask, request, jsonify
from googlesearch import search

# app = Flask(__name__)


search_engines = {
    "Google": "",
    "GitHub": "site:github.com",
    "Reddit": "site:reddit.com",
    "Wikipedia": "site:https://en.wikipedia.org/wiki",
}


def Search(query, site_query="", num_results=10):
    query = f"{query} {site_query}".strip()
    search_results = list(search(query, num_results=num_results, advanced=True))
    return search_results


# @app.route("/api/search", methods=["POST"])
def search_api(data):   
    # data = request.get_json()
    query = data.get("query", "python")  # Default query
    selected_engine = data.get("engine", "Google")  # Default search engine

    site_query = search_engines.get(selected_engine, "")
    num_results = data.get("num_results", 10)
    search_results = Search(query, site_query, num_results=num_results)

    # Convert the search results to a JSON response
    response = [{"title": result.title, "url": result.url} for result in search_results]
    return (response)

# @app.route("/api/search/<file_type>", methods=["POST"])
def search_by_file_type_api(file_type, data):
    query = data.get("query", "python")  # Default query
    selected_engine = data.get("engine", "Google")  # Default search engine
    site_query = search_engines.get(selected_engine, "")
    num_results = data.get("num_results", 10)
    search_results = Search(query, site_query, num_results=num_results, file_type=file_type)

    # Convert the search results to a JSON response
    response = [{"title": result.title, "url": result.url} for result in search_results]
    return (response)


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
