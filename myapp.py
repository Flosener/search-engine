from flask import Flask, request, render_template
from crawler import Crawler

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("search.html")

@app.route("/search")
def search():
    if not 'input' in request.args:
        return "Something went wrong."
    else:
        query = request.args['input']
        index = Crawler.crawl()
        results = Crawler.search(query, index)
        return render_template("results.html", results=results)