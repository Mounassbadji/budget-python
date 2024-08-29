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
class Montant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

@app.route('/ajout_revenus', methods=['GET', 'POST'])
def ajout_revenus():
    if request.method == 'POST':
        montant = request.form.get('montant')
        description = request.form.get('description')
        try:
            montant = Montant(value=float(montant), description=description)
            db.session.add(montant)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            return f"Une erreur s'est produite: {str(e)}"
    return render_template('ajout_revenus.html')

@app.route('/ajout_depenses', methods=['GET', 'POST'])
def ajout_depenses():
    if request.method == 'POST':
        montant = request.form.get('montant')
        description = request.form.get('description')
        try:
            montant = Montant(value=-float(montant), description=description)  # Les dépenses sont des valeurs négatives
            db.session.add(montant)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            return f"Une erreur s'est produite: {str(e)}"
    return render_template('ajout_depenses.html')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
