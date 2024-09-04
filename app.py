from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modèles de la base de données
class Montant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

class Depense(db.Model):
    __tablename__ = 'depenses' 
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False)

    def __init__(self, description, montant):
        self.description = description
        self.montant = montant

class Revenu(db.Model):
    __tablename__ = 'revenus'  
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=False) 

    def __init__(self, description, montant):
        self.description = description
        self.montant = montant    

# Route pour la page d'accueil
@app.route('/')
def index():
    depenses = Depense.query.all()  
    revenus = Revenu.query.all()  
    return render_template('index.html', depenses=depenses, revenus=revenus)

# Route pour ajouter un revenu
@app.route('/ajout_revenus', methods=['GET', 'POST'])
def ajout_revenus():
    if request.method == 'POST':
        montant = request.form.get('montant')
        description = request.form.get('description')
        try:
            revenu = Revenu(description=description, montant=float(montant))  
            db.session.add(revenu)
            db.session.commit()
            return redirect(url_for('index'))  # Redirige vers la page d'accueil
        except Exception as e:
            db.session.rollback()
            return f"Une erreur s'est produite: {str(e)}"
    return render_template('ajout_revenus.html')

# Route pour ajouter une dépense
@app.route('/ajout_depenses', methods=['GET', 'POST'])
def ajout_depenses():
    if request.method == 'POST':
        montant = request.form.get('montant')
        description = request.form.get('description')
        try:
            depense = Depense(description=description, montant=float(montant))  
            db.session.add(depense)
            db.session.commit()
            return redirect(url_for('index'))  # Redirige vers la page d'accueil
        except Exception as e:
            db.session.rollback()
            return f"Une erreur s'est produite: {str(e)}"
    return render_template('ajout_depenses.html')

# Route pour supprimer un revenu
@app.route('/delete_revenu/<int:id>', methods=['POST'])
def delete_revenu(id):
    revenu = Revenu.query.get_or_404(id)
    db.session.delete(revenu)
    db.session.commit()
    return redirect(url_for('index'))

# Route pour supprimer une dépense
@app.route('/delete_depense/<int:id>', methods=['POST'])
def delete_depense(id):
    depense = Depense.query.get_or_404(id)
    db.session.delete(depense)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
