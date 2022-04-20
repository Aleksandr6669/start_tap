from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_user,login_required, logout_user

from serverf.init import app 
from serverf.init import db
from serverf.modls import Article, User, Messagers, Useron



@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/<url>')
def url(url):
    return redirect('/log')

@app.route('/posts')
@login_required
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/admin')
def admin():
    user = User.query.order_by(User.date.desc()).all()
    return render_template("admin.html", user=user)


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





@app.route('/delete/<int:id>',)
@login_required
def post_delete(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/posts')

@app.route('/delete_user/<int:id>',)
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin')



@app.route('/posts/<int:id>', methods=['POST', 'GET'])
@login_required
def post_d(id):
    article = Article.query.get(id)
    return render_template("post_d.html", article=article)

@app.route('/log/<int:id>', methods=['POST', 'GET'])
@login_required
def lk(id):
    user = User.query.get(id)

    messager = Messagers.query.filter_by(user = user.user_name).order_by(Messagers.date.desc()).all()
    return render_template("lk.html", user=user, messager=messager)

@app.route('/users/<int:id>', methods=['POST', 'GET'])
def users(id):
    user = User.query.get(id)
    return render_template("users.html", user=user)

@app.route('/aboud')
def aboud():
    return render_template("aboud.html")

@app.route('/log/', methods=['POST', 'GET'])
@app.route('/log', methods=['POST', 'GET'])
def log():
    if request.method == "POST" :
        user_name = request.form['user_name']
        password = request.form['password']
        renainma = request.form.get('renainma')
        user = User.query.filter_by(user_name = user_name).first()
        if len(user_name)>4 and len(password)>4:             
            if not user:
                flash ('Такого пользователя нет')
                return redirect('/reg')
            else:
                if check_password_hash(user.password, password):
                    login_user(user)
                    us = {'id': user.id, 'name': user.name, 'user_name': user.user_name}
                    session['us'] = us
                    session.modified = True
                    next_url =  request.args.get ('next')
                    if renainma:
                        session.permanent = True
                    else:
                        session.permanent = False
                    if not next_url:
                        return redirect('/log/'+str(user.id))
                    else:
                        return redirect (next_url) 
                else: 
                    flash ('Не верный пароль')
                    return redirect('/log')
            
                    
        else:
            flash ('Не коректно ввелины данные')
            return render_template("log.html")
    else: 
        if 'us' not in session:    
            return render_template("log.html")
        else:
            return redirect('/log/'+str(session.get('us').get('id')))
@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == "POST" :
        name = request.form['name']
        user_name = request.form['user_name']
        password = request.form['password']
        repeed_password = request.form['repeed_password']
        if len(name) > 4 and len(user_name)>4\
            and len(password)>4 and password == repeed_password:
            hash = generate_password_hash(password)
            user = User(name=name, user_name=user_name, password=hash)
            userinf = User.query.filter_by(user_name = user_name).first()
            if user:
                if not userinf:
                    db.session.add(user)
                    db.session.commit()
                    flash ('Для того чтобы продолжить необходими ввойти')
                    return redirect(url_for('log'))
                else:
                    flash ('Пользователь уже есть')
                    return redirect(url_for('reg'))
            else:
                flash ('Ошибка при регистрации!')
                return redirect(url_for('reg'))
        else:
            flash ('Неверно заполнены поля')
            return redirect(url_for('reg'))
            #return render_template("reg.html")
    else:
        
        return render_template("reg.html")


    
    
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    session.pop('us', None)
    
    return redirect(url_for('index'))

@app.route('/create_article', methods=['POST', 'GET'])
@login_required
def create_article():
    if request.method == "POST" :
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            flash('Статья добавлена')
            # return redirect('/create_article', msgq="Ntcn")
        except:
            flash('При добавлении статьи произошла ошибка!')
            flash ('Пользователь уже есть')
    return render_template("create_article.html")

@app.route('/messager/<user_name>/<user>', methods=['POST', 'GET'])
@app.route('/messager/<user_name>/<user>/', methods=['POST', 'GET'])
@login_required
def messager(user_name, user): 
    if request.method == "POST" :
        # user = request.args.get('user_name')
        # user_mess= request.args.get('user')
        messager = request.form['msg']
        messagers = Messagers(user=user_name, user_mess=user, messager=messager)

        try:
            db.session.add(messagers)
            db.session.commit()
            flash('Сообщение отправлено')
            return redirect('/log')
        except:
            flash('При отправки сообщения произошла ошибка!')
            return redirect('/log')
    return render_template("messager.html", user=user_name, user_mess=user)


@app.route('/create_messager/<int:id>', methods=['POST', 'GET'])
@login_required
def create_messager(id):
    if request.method == "POST" :
        user_name = str(session.get('us').get('user_name'))
        user = request.form['user']
        messager = request.form['msg']
        messagers = Messagers(user=user, user_mess=user_name, messager=messager)

        try:
            db.session.add(messagers)
            db.session.commit()
            flash('Сообщение отправлено')
            return redirect('/log')
        except:
            flash('При отправки сообщения произошла ошибка!')
            return redirect('/log')
    user_name = str(session.get('us').get('user_name'))
    return render_template("create_messager.html", user_mess=user_name)





#@app.after_request
#def redirect_to_signin(response):
    #if response.status_code == 401:
        #return redirect(url_for('log') + '?next='+ request.url)
    #else:
        #return response


