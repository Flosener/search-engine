# Import necessary packages
import requests
from bs4 import BeautifulSoup


def search(query, index):
    """
    This function takes a list of words as a parameter and returns (by using the index) a list of links to all pages that contain all the words from the list.

    Args:
    query -- a string of words separated by a space
    index -- an index that contains all the crawled web content
    """
    # catch exception
    if type(query) != str:
        print(f"Please provide a string, not {type(query)}.")
        query = str(query)
        #return
    
    # split the query into single words
    words = query.split()
    results = []
    dummy = []

    # iterate over words in the query and get the location url
    for idx, word in enumerate(words):
        word = word.lower()

        # catch KeyError
        try:
            for url in index[word]:
                # all urls of the first query word are saved in results
                if idx == 0:
                    results.append(url[0])
                # apply AND to only keep urls where all words appear
                elif url in results:
                    dummy.append(url)
                    results = [url for url in dummy if url in results]
                    dummy = []
        except KeyError:
            print(f"There is no {word} in the index.")
            return

    return results




# Initialize index as dictionary
index = {}

# Initialize working stack
domain = "https://vm009.rz.uos.de/crawl/"
source = domain + "index.html"
stack = [source]
visited = []

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
            content = soup.body.text
            words = content.split()

            # Update index
            for word in words:
                word = word.lower() # convert to lowercase
                # ChatGPT: https://chat.openai.com/share/f7469407-09b5-426a-9354-03bd23445a8b
                if word not in index:
                    index[word] = [(stack[0], 1)]  # Initialize with a list containing the location and count
                else:
                    # Find the last entry in the list
                    last_entry = index[word][-1]
                    # Check if the word appeared at the same location
                    if last_entry[0] == stack[0]:
                        # Increment the count
                        index[word][-1] = (stack[0], last_entry[1] + 1)
                    else:
                        # Add a new entry for the word at the current location
                        index[word].append((stack[0], 1))

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

# test search functionality
results = search("welcome to the home page", index)
print(results)