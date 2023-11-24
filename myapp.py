from flask import Flask, request, render_template
from crawler import Crawler
import os
from whoosh.index import open_dir
import traceback

app = Flask(__name__)
indexdir = os.listdir("indexdir")

@app.errorhandler(500)
def internal_error(exception):
   return "<pre>"+traceback.format_exc()+"</pre>"

@app.route("/")
def start():
    return render_template("search.html")

@app.route("/search")
def search():
    if not 'input' in request.args:
        return "Something went wrong."
    else:
        query = request.args['input']
        # if the index is built already, do not crawl again
        if len(indexdir) == 0:
            index = Crawler.crawl()
        else:
            index = open_dir("indexdir")
        results = Crawler.search(query, index)

        return render_template("results.html", results=results)