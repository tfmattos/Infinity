from . import db
from datetime import datetime

class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    resultados_financeiros = db.Column(db.Text, nullable=True)
    # Relacionamento: Um projeto possui várias features
    features = db.relationship('Feature', backref='projeto', lazy=True)

    def __repr__(self):
        return f'<Projeto {self.nome}>'

class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    # Relacionamento: Uma feature possui várias tasks
    tasks = db.relationship('Task', backref='feature', lazy=True)

    def __repr__(self):
        return f'<Feature {self.nome} in Projeto {self.projeto_id}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.nome} in Feature {self.feature_id}>'
