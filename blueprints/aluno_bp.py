from flask import *
from blueprints.admin_bp import admin_bp
from database.database import *
from models.modelosDB import *
from werkzeug.utils import secure_filename
import os
aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')


@aluno_bp.route('/aluno', methods=['GET', 'POST'])
def aluno_pagina():
    email = session.get('user')
    if not email or session.get('role') != 'aluno':
        flash("Faça login para acessar a página do aluno.")
        return redirect(url_for('login'))

    aluno = aluno_dao.buscar_por_email(email)

    acoes = acao_dao.listar_todas()

    return render_template('aluno/aluno.html', aluno=aluno, acoes=acoes)

@aluno_bp.route('/enviar_acao', methods=['POST'])
def enviar_acao():
    if 'user' not in session or session.get('role') != 'aluno':
        flash("Faça login como aluno para enviar uma ação.")
        return redirect(url_for('login'))

    email_aluno = session['user']
    id_acao = request.form.get('acao')
    comentarios_aluno = request.form.get('mensagem')
    link_aluno = request.form.get('link')  # <- novo campo

    if not id_acao or not comentarios_aluno or not link_aluno:
        flash("Preencha todos os campos obrigatórios.")
        return redirect(url_for('aluno.aluno_pagina'))

    nova_acao = AcaoRealizadaAlunoDB(
        email_aluno=email_aluno,
        id_acao=id_acao,
        comentarios_aluno=comentarios_aluno,
        link=link_aluno,
        valor=0,
        status='pendente'
    )

    acao_realizadasDAO.adicionar(nova_acao)

    flash("Ação enviada com sucesso e aguarda avaliação!")
    return redirect(url_for('aluno.aluno_pagina'))

@aluno_bp.route("/compras_disponiveis")
def compras_disponiveis():
    return render_template("aluno/compras_disponiveis.html")


@aluno_bp.route("/historico_acoes")
def historico_acoes():
    return "<h1>Histórico de ações</h1>"