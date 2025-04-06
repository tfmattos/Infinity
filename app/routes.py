from flask import Blueprint, request, jsonify
from . import db
from .models import Projeto, Feature, Task
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Bem-vindo à Plataforma de Gerenciamento de Projetos!"

# ---------------------------------------------------
# Endpoints para Gerenciamento de Projetos
# ---------------------------------------------------

@main.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    novo_projeto = Projeto(
        nome=data.get('nome'),
        descricao=data.get('descricao'),
        resultados_financeiros=data.get('resultados_financeiros')
    )
    db.session.add(novo_projeto)
    db.session.commit()
    
    # Se o formulário incluir features iniciais, cria cada uma
    features_data = data.get('features', [])
    for feat in features_data:
        nova_feature = Feature(
            projeto_id=novo_projeto.id,
            nome=feat.get('nome'),
            descricao=feat.get('descricao')
        )
        db.session.add(nova_feature)
        db.session.commit()
        
        # Se a feature incluir tasks (backlog)
        tasks_data = feat.get('tasks', [])
        for task_data in tasks_data:
            nova_task = Task(
                feature_id=nova_feature.id,
                nome=task_data.get('nome'),
                descricao=task_data.get('descricao'),
                status=task_data.get('status', 'pending')
            )
            db.session.add(nova_task)
    db.session.commit()
    return jsonify({'message': 'Projeto criado', 'project_id': novo_projeto.id}), 201

@main.route('/projects', methods=['GET'])
def get_projects():
    projetos = Projeto.query.all()
    projects_list = []
    for projeto in projetos:
        projects_list.append({
            'id': projeto.id,
            'nome': projeto.nome,
            'descricao': projeto.descricao,
            'resultados_financeiros': projeto.resultados_financeiros
        })
    return jsonify(projects_list)

@main.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    projeto = Projeto.query.get_or_404(project_id)
    features_list = []
    for feature in projeto.features:
        features_list.append({
            'id': feature.id,
            'nome': feature.nome,
            'descricao': feature.descricao
        })
    project_data = {
        'id': projeto.id,
        'nome': projeto.nome,
        'descricao': projeto.descricao,
        'resultados_financeiros': projeto.resultados_financeiros,
        'features': features_list
    }
    return jsonify(project_data)

@main.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    projeto = Projeto.query.get_or_404(project_id)
    data = request.get_json()
    projeto.nome = data.get('nome', projeto.nome)
    projeto.descricao = data.get('descricao', projeto.descricao)
    projeto.resultados_financeiros = data.get('resultados_financeiros', projeto.resultados_financeiros)
    db.session.commit()
    return jsonify({'message': 'Projeto atualizado'})

@main.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    projeto = Projeto.query.get_or_404(project_id)
    db.session.delete(projeto)
    db.session.commit()
    return jsonify({'message': 'Projeto deletado'})

# ---------------------------------------------------
# Endpoints para Gerenciamento de Features
# ---------------------------------------------------

@main.route('/projects/<int:project_id>/features', methods=['POST'])
def create_feature(project_id):
    # Verifica se o projeto existe
    Projeto.query.get_or_404(project_id)
    data = request.get_json()
    nova_feature = Feature(
        projeto_id=project_id,
        nome=data.get('nome'),
        descricao=data.get('descricao')
    )
    db.session.add(nova_feature)
    db.session.commit()
    return jsonify({'message': 'Feature criada', 'feature_id': nova_feature.id}), 201

@main.route('/projects/<int:project_id>/features', methods=['GET'])
def get_features(project_id):
    Projeto.query.get_or_404(project_id)
    features = Feature.query.filter_by(projeto_id=project_id).all()
    features_list = []
    for feature in features:
        features_list.append({
            'id': feature.id,
            'nome': feature.nome,
            'descricao': feature.descricao
        })
    return jsonify(features_list)

@main.route('/features/<int:feature_id>', methods=['GET'])
def get_feature(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    tasks_list = []
    for task in feature.tasks:
        tasks_list.append({
            'id': task.id,
            'nome': task.nome,
            'descricao': task.descricao,
            'status': task.status,
            'data': task.data.isoformat()
        })
    feature_data = {
        'id': feature.id,
        'nome': feature.nome,
        'descricao': feature.descricao,
        'tasks': tasks_list
    }
    return jsonify(feature_data)

@main.route('/features/<int:feature_id>', methods=['PUT'])
def update_feature(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    data = request.get_json()
    feature.nome = data.get('nome', feature.nome)
    feature.descricao = data.get('descricao', feature.descricao)
    db.session.commit()
    return jsonify({'message': 'Feature atualizada'})

@main.route('/features/<int:feature_id>', methods=['DELETE'])
def delete_feature(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    db.session.delete(feature)
    db.session.commit()
    return jsonify({'message': 'Feature deletada'})

# ---------------------------------------------------
# Endpoints para Gerenciamento de Tasks (Backlog)
# ---------------------------------------------------

@main.route('/features/<int:feature_id>/tasks', methods=['POST'])
def create_task(feature_id):
    Feature.query.get_or_404(feature_id)
    data = request.get_json()
    nova_task = Task(
        feature_id=feature_id,
        nome=data.get('nome'),
        descricao=data.get('descricao'),
        status=data.get('status', 'pending')
    )
    db.session.add(nova_task)
    db.session.commit()
    return jsonify({'message': 'Task criada', 'task_id': nova_task.id}), 201

@main.route('/features/<int:feature_id>/tasks', methods=['GET'])
def get_tasks(feature_id):
    Feature.query.get_or_404(feature_id)
    tasks = Task.query.filter_by(feature_id=feature_id).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task.id,
            'nome': task.nome,
            'descricao': task.descricao,
            'status': task.status,
            'data': task.data.isoformat()
        })
    return jsonify(tasks_list)

@main.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_data = {
        'id': task.id,
        'nome': task.nome,
        'descricao': task.descricao,
        'status': task.status,
        'data': task.data.isoformat()
    }
    return jsonify(task_data)

@main.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.nome = data.get('nome', task.nome)
    task.descricao = data.get('descricao', task.descricao)
    task.status = data.get('status', task.status)
    task.data = datetime.utcnow()  # Atualiza a data de modificação
    db.session.commit()
    return jsonify({'message': 'Task atualizada'})

@main.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deletada'})
