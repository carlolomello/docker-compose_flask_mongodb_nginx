from flask import Flask, request, render_template
from flask_pymongo import PyMongo
import os

application = Flask(__name__, static_url_path='', static_folder='static')


mongo_conn_uri = 'mongodb://' +\
    os.environ['MONGODB_USERNAME'] +\
    ':' + os.environ['MONGODB_PASSWORD'] +\
    '@' + os.environ['MONGODB_HOSTNAME'] +\
    ':27017/' + os.environ['MONGODB_DATABASE']

application.config["MONGO_URI"] = mongo_conn_uri
mongo = PyMongo(application)
db = mongo.db

@application.route("/")
def index():
    return render_template("src/homepage.html")

@application.route("/register")
def register():
    return render_template("src/register_page.html")

@application.route('/register_conf')
def register_conf():
    username = request.args.get("username")
    password = request.args.get("password")
    nome = request.args.get("nome")
    cognome = request.args.get("cognome")
    telefono = request.args.get("telefono")
    
    item = {
        'username': username,
        'password': password,
        'nome': nome,
        'cognome': cognome,
        'telefono': telefono
    }
    db.persona.insert_one(item)

    return render_template("src/homepage.html")



@application.route("/login")
def login():
    return render_template("src/login_page.html")

@application.route('/logged_in')
def logged_in():
    username = request.args.get("username")
    password = request.args.get("password")
    
    _persona = db.persona.find({
        'username': username,
        'password': password
        })

    item = {}
    data = []

    for pers_temp in _persona:
        item = {
            'nome': pers_temp['nome'],
            'cognome': pers_temp['cognome'],
            'telefono': pers_temp['telefono']
        }
        data.append(item)
        
    for pers_temp in data:
        nome = pers_temp['nome']
        cognome = pers_temp['cognome']
        telefono = pers_temp['telefono']

    return render_template('src/welcome.html', nome = nome, cognome = cognome, telefono = telefono)

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)