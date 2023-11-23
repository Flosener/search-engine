# Import necessary packages
import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

class Crawler():

    def search(query, index):
        """
        This function takes a list of words as a parameter and returns (by using the index) a list of links to all pages that contain all the words from the list.

        Args:
        query -- a string of words separated by a space
        index -- an index that contains all the crawled web content
        """
        res = []

        # type cast to string if necessary
        if type(query) != str:
            query = str(query)
        
        with index.searcher() as searcher:
            # search for query in index
            query = QueryParser("content", index.schema).parse(query)
            results = searcher.search(query)

            # print all results
            for r in results:
                res.append({'url': r['url'], 'title': r['title'], 'content': r['content']})

        return res

    def crawl():
        # Initialize vars
        domain = "https://vm009.rz.uos.de/crawl/"
        source = domain + "index.html"
        stack = [source]
        visited = []

        schema = Schema(url=TEXT(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))

        # Create an index in the directory indexdr (the directory must already exist!)
        ix = create_in("indexdir", schema)
        writer = ix.writer()

        # Continue crawling until all subpages are crawled
        while len(stack) > 0:

            # If current page was not visited, get it
            if stack[0] not in visited:

                # Get the website and check status
                response = requests.get(stack[0], timeout=5)
                print(f"Current website: {stack[0]}, Status: {response.status_code}")

                if response.status_code == 200:
                    # Parse content
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.head.text
                    content = soup.body.text
                    #words = content.split()

                    # Update the index
                    writer.add_document(url=stack[0], title=title, content=content)

                    # Push new links to work stack
                    for link in soup.find_all('a'):
                        url = link.get('href')
                        if domain not in url:
                            if 'http' not in url:
                                url = domain + url
                            else:
                                continue
                        if url not in visited:
                            stack.append(url)

                    # Update visited
                    visited.append(stack[0])

            # remove current page from work stack
            stack.remove(stack[0])
            print(f"Stack left: {stack}")
            print(f"Visited websites: {visited}")

        writer.commit()

        # return the index
        return ix