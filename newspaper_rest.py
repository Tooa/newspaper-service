from flask import Flask, Response

from validator import *
from authentication import *
from util import *

from newspaper import Article

activate_schema = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "language": {"type": "string"},
    },
    "required": ["url", "language"]
}

app = Flask(__name__)
app.config['activate_schema'] = activate_schema


@app.route('/v1/extract', methods=['POST'])
@requires_auth
@validate_json
@validate_schema('activate_schema')
def extract():
    if request.headers['Content-Type'] == 'application/json':
        input = request.json

        article = Article(input["url"], language=input["language"])
        article.download()
        article.parse()
        article.nlp()

        response = article_to_json(article)

        resp = Response(response, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://www.tooa.github.io'

        return resp
    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main__':
    app.run(debug=True)

"""
curl -i -u "guest:guest" -H "Content-type: application/json" -X POST http://127.0.0.1:5000/v1/extract -d '{ "url": "http://www.nytimes.com/2015/02/10/nyregion/kabul-chawla-bptp-india-real-estate-manhattan.html?hp&action=click&pgtype=Homepage&module=a-lede-package-region&region=top-news&WT.nav=top-news", "language": "en"}'
"""
