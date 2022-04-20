from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_user,login_required, logout_user

from serverf.init import app 
from serverf.init import db
from serverf.modls import Article, User, Messagers






@app.route('/log_t', methods=['POST', 'GET'])
def log_t():
    if request.method == "POST" :
        req = request.get_json(force=True)
        user_name = req.get('user_name')
        password = req.get('password')
        renainma = False
        user = User.query.filter_by(user_name = user_name).first()
        if len(user_name)>4 and len(password)>4:
             
            if not user:
                return  "Зарегестрируйтесь"
            else:
                if check_password_hash(user.password, password):
                    login_user(user)
#                     us = {'id': user.id, 'name': user.name, 'user_name': user.user_name}
#                     session['us'] = us
#                     session.modified = True
#                     if renainma:
#                         session.permanent = True
#                     else:
#                         session.permanent = False
                
                    return str(session) 
                else: 
                    return "Не верный пароль "
        else:
            return "Не коректно ввелины данные " 
    else:
        return "Нужен пост запрос"



@app.route('/reg_t', methods=['POST'])
def reg_t():
    req = request.get_json(force=True)
    name = req.get('name')
    user_name = req.get('user_name')
    password = req.get('password')
    repeed_password = req.get('repeed_password')
    if len(name) > 4 and len(user_name)>4\
         and len(password)>4 and password == repeed_password:
         hash = generate_password_hash(password)
         user = User(name=name, user_name=user_name, password=hash)
         userinf = User.query.filter_by(user_name = user_name).first()
         if user:
             if not userinf:
                 db.session.add(user)
                 db.session.commit()   
                 return "Зарегестрирован"
             else:
                return "Пользователь уже есть"
         else:
            return "Ошибка при регистрации!"
    else:
        return "Неверно заполнены поля"


    
    
@app.route('/logout_t', methods=['POST', 'GET'])
def logout_t():
    logout_user()
    session.pop('us', None)
    return "Вы вышли"

@app.route('/create_messager_t', methods=['POST', 'GET'])
@login_required
def create_messager_t():
    if request.method == "POST" :
        messager = request.get_json(force=True)
        user_name = session.get('us').get('user_name')
        user = messager.get('user')
        messager = messager.get('msg')
        messagers = Messagers(user=user, user_mess=user_name, messager=messager)
        if not user_name:
            return "Сначало войдите"
        else:
            try:
                db.session.add(messagers)
                db.session.commit()

                return "Сообщение отправлено: От "+ user_name+" Пользователю: " + user
            except:
                return "При отправки сообщения произошла ошибка!"  
    user_name = str(session.get('us').get('user_name'))
    return "Для пользователя "+user_name+"нужен пост запрос"



@app.route('/user', methods=['POST', 'GET'])
@login_required
def user():
    if request.method == "POST" :
        user_id = session.get('_user_id')
        user = User.query.get(user_id)
        if not user_id:
            return "Error"
        else:
            return str(user.user_name)
            


#articles = Article.query.order_by(Article.date.desc()).all()
#user = User.query.get(id)
#article = Article.query.get(id)



