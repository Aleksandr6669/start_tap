from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hashlib import md5
import time
from google.cloud import dialogflow
from werkzeug.utils import redirect
import os
import asyncio
import requests


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="viktoriya-50dd3-7e1f4b6de7bd.json"

session_client = dialogflow.SessionsClient()
project_id = 'viktoriya-50dd3'
session_id = 'sessions2'
language_code = 'ru'
session = session_client.session_path(project_id, session_id)




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/token', methods=['POST', 'GET'])
def token():
    if request.method == "POST" :
        title = request.args['title']
        intro = request.args['intro']
        text = request.args['text']

        article = Article(title=title, intro=intro, text=text)
        db.session.add(article)
        db.session.commit()
        return "OK"

    elif request.method == "GET" :
        ids = request.args['id']
        article = Article.query.get(ids)
        return  "Статья: " + article.title + " Текст: " + article.text


@app.route('/url', methods=['GET', 'POST'])
def url():
   if request.args['text'].lower() == 'начали':
        return "123445"
   elif request.args['text'].lower() == 'конец':
        return "000000"
   else:
        text_input = dialogflow.TextInput(
                text=request.args['text'], language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        if response.query_result.fulfillment_text:
           return  response.query_result.fulfillment_text
        else:
           return "Я тебя не понимаю"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
        req = request.get_json(force=True)
        r_r=req.get('queryResult')
        r_r2=r_r.get('action')
        ids = r_r.get('parameters').get('Kelly')
        title = r_r.get('parameters').get('Title')
        intro = r_r.get('parameters').get('Intro')
        text = r_r.get('parameters').get('Text')
        if r_r2 == 'input.post':
            article = Article.query.get(ids)
            return {'fulfillmentText': 'Статья: ' + article.title + ' Текст: ' + article.text}
        elif r_r2 == 'Addpost.Addpost-yes':
            article = Article(title=title, intro=intro, text=text)
            db.session.add(article)
            db.session.commit()
            return  {'fulfillmentText': 'Добавила'}
        elif r_r2 == 'televizor':
            response = requests.get('https://maker.ifttt.com/trigger/tvonoff/with/key/bmlbNYGWkYkYXyjjbG2T85')
            return  {'fulfillmentText': 'Окей готово'}
    # # return make_response(jsonify(req()))

@app.route('/delete/<int:id>',)
def post_delete(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/posts')



@app.route('/posts/<int:id>', methods=['POST', 'GET'])
def post_d(id):
    article = Article.query.get(id)
    return render_template("post_d.html", article=article)

@app.route('/aboud')
def aboud():
    return render_template("aboud.html")

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST" :
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка!"
    else:
        return render_template("create-article.html")



if __name__=="__main__":
    app.run(debug=True)

