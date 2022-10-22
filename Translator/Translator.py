from flask.templating import render_template
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, url_for, redirect
import regex
app = Flask(__name__)

@app.route("/")
def index():
    word = request.args.get('word', default = 'mersi', type = str)
    return render_template('header.html') + search(word)

@app.route(("/wiki/<Word>"))
def translate(Word):
    return redirect(url_for('index', word=Word))
    
@app.route('/', methods=['POST'])
def redirection():
    text = request.form['text']
    return redirect(url_for('index', word=text))

@app.errorhandler(404)
def page_not_found(e):
    return "URL '<strong>" + request.path + "</strong>' does not exist. Click <a href='/'>here</a> to go back."
def search(word):

    URL = "https://en.wiktionary.org/wiki/" + word.lower()

    page = requests.get(URL);

    soup = BeautifulSoup(page.content, "html.parser")

    initialResults = soup.find(id="Romanian")

    if initialResults == None:
        return "Romanian interpretation not found"

    initialResults = initialResults.parent

    currentElement = initialResults.next_sibling
    try:
        totals = "<H1>" + word.capitalize().replace("_", " ") + "<H1>" + str(currentElement.prettify())
    except:
        totals = "<H1>" + word.capitalize().replace("_", " ") + "<H1>" + str(currentElement)

    while True:
        try:
            currentElement = currentElement.next_sibling
        except:
            return totals

        if "<h3>" in str(currentElement):
            totals = totals + "<h3>" + str(currentElement.getText().replace("[edit]", "")) + "</h3>"
            continue
        if "redlink" in str(currentElement) and not "Declension" in str(currentElement):
            totals = totals + str(currentElement.getText())
            continue
        if "phrasebook NavFrame" in str(currentElement):
            continue
        if "<hr/>" in str(currentElement) or "Parsed by" in str(currentElement):
            break
        try:
            totals = totals + str(currentElement.prettify())
        except:
            totals = totals + str(currentElement)

    return str(totals)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)