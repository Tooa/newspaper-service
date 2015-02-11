from flask import json


def article_to_json(article):
    result = {'title': article.title, 'text': article.text, 'authors': article.authors,
              'publish_date': article.publish_date, 'top_image': article.top_image, 'keywords': article.keywords,
              'summary': article.summary}

    return json.dumps(result)
