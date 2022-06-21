# все импорты
import email
from email import message
from unicodedata import name
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, jsonify
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_mail import Mail,Message
from sqlalchemy import false

app = Flask(__name__)
db = SQLAlchemy()  
DB_NAME = "database.db" 
app.config['DEBUG'] = True
app.config['MAIL_SERVER']='smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'user@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# создание и настройка приложения
def create_app():
    # конфигурация
    app.config['SECRET_KEY'] = 'qupya_sozdi_eshkim_tappaydi'   #Секретный ключ.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #конфигурационный ключ для определения URI базы данных
    db.init_app(app)
  

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)   #Создание БД

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader #загружения пользователя
    def load_user(id):
        return User.query.get(int(id))

    return app


@app.route('/send_message', methods=['GET', 'POST']) #декоратор маршрутизации
@login_required
def send_message():
    if request.method == "POST":
       # name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['message']

        message = Message(subject, sender="user@yandex.ru", recipients=[email])
        message.body = msg
        mail.send(message)
        success = "Message sent"

    return render_template("result.html", success=success)

@app.route('/Creator', methods=['GET', 'POST']) #декоратор маршрутизации
@login_required
def Creator():
    return render_template("creator.html", user=current_user)  #поставлятет файлы шаблонов HTML

@app.route('/Python', methods=['GET', 'POST']) #декоратор маршрутизации
@login_required
def Python():
    return render_template("python.html", user=current_user)  #поставлятет файлы шаблонов HTML

@app.route('/CPP', methods=['GET', 'POST'])
@login_required
def CPP():
    return render_template("cpp.html", user=current_user)

@app.route('/Java')
@login_required
def Java():
    return render_template("java.html", user=current_user)

@app.errorhandler(404) #ошибка 404
def page_not_found(e):
    return render_template('404.html', user=current_user)


def create_database(app):        #Создание БД
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
