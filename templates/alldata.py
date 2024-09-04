from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Définition du modèle
class alldata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    
@app.route('/console')
def console():
    alldatas = alldata.query.all()
    for data in alldatas:
        print(f'ID: {data.id}, Value: {data.value}, Description: {data.description}')
    return "Data printed in the console!"
