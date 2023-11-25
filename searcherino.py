from flask import Flask, request, render_template
from crawler import search_ix, crawl
from whoosh.index import open_dir
import os

app = Flask(__name__)

# create an 'indexdir' folder if it does not exist (important for saving content to index with Flask)
if not os.path.isdir('indexdir'):
        os.mkdir('indexdir')
indexdir = os.listdir("indexdir")

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
            index = crawl()
        else:
            index = open_dir("indexdir")
        results = search_ix(query, index)

        return render_template("results.html", results=results)