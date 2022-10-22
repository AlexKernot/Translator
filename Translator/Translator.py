
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
    print("Hello")
    return '<form method="POST"> <input name="text" type="text"> </form>' + search("mersi")

@app.route(("/wiki/<Word>"))
def translate(Word):
    return search(Word)
    
@app.route('/', methods=['POST'])
def redirect():
    text = request.form['text']
    return '<form method="POST"> <input name="text" type="text"> </form>' + search(text)

def search(word):

    URL = "https://en.wiktionary.org/wiki/" + word

    page = requests.get(URL, verify = False);

    soup = BeautifulSoup(page.content, "html.parser")

    initialResults = soup.find(id="Romanian")

    if initialResults == None:
        return "Romanian interpretation not found"

    initialResults = initialResults.parent

    currentElement = initialResults.next_sibling
    try:
        totals = str(initialResults.prettify()) + str(currentElement.prettify())
    except:
        totals = str(initialResults.prettify()) + str(currentElement)

    while True:
        try:
            currentElement = currentElement.next_sibling
        except:
            return totals
        if "<hr/>" in str(currentElement) or "NewPP" in str(currentElement):
            break
        try:
            totals = totals + str(currentElement.prettify())
        except:
            totals = totals + str(currentElement)


    return(str(totals))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)