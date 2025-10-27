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

@aluno_bp.route("/historico_acoes")
def historico_acoes():
    email = session.get('user')
    if not email or session.get('role') != 'aluno':
        flash("Faça login para acessar o histórico.")
        return redirect(url_for('login'))

    acoes_aprovadas = acao_realizadasDAO.listar_aprovadas_por_aluno(email)
    acoes_pendentes = acao_realizadasDAO.listar_pendentes_por_aluno(email)
    acoes_rejeitadas = acao_realizadasDAO.listar_rejeitadas_por_aluno(email)

    return render_template(
        "aluno/aluno_historico_acoes.html",
        acoes_aprovadas=acoes_aprovadas,
        acoes_pendentes=acoes_pendentes,
        acoes_rejeitadas=acoes_rejeitadas
    )

''
@aluno_bp.route('/enviar_acao', methods=['POST'])
def enviar_acao():
    if 'user' not in session or session.get('role') != 'aluno':
        flash("Faça login como aluno para enviar uma ação.")
        return redirect(url_for('login'))

    email_aluno = session['user']
    aluno = aluno_dao.buscar_por_email(email_aluno)

    # 🚨 Verifica se o aluno ainda existe
    if not aluno:
        session.clear()
        flash("Sua conta de aluno não existe mais. Faça login novamente.")
        return redirect(url_for('login'))

    id_acao = request.form.get('acao')
    comentarios_aluno = request.form.get('mensagem')
    link_aluno = request.form.get('link')

    if not id_acao or not comentarios_aluno or not link_aluno:
        flash("Preencha todos os campos obrigatórios.")
        return redirect(url_for('aluno.aluno_pagina'))

    acao = acao_dao.buscar_por_id(id_acao)
    nova_acao = AcaoRealizadaAlunoDB(
        email_aluno=email_aluno,
        id_acao=id_acao,
        comentarios_aluno=comentarios_aluno,
        link=link_aluno,
        valor=acao.valor,
        status='pendente'
    )

    try:
        acao_realizadasDAO.adicionar(nova_acao)
        flash("Ação enviada com sucesso e aguarda avaliação!")
    except Exception as e:
        flash(f"Erro ao enviar ação: {e}")
    return redirect(url_for('aluno.aluno_pagina'))



@aluno_bp.route("/retirar_recompensas")
def retirar_recompensas():
    if 'user' not in session or session.get('role') != 'aluno':
        flash("Faça login como aluno para acessar esta página.")
        return redirect(url_for('login'))

    email_aluno = session['user']
    aluno = aluno_dao.buscar_por_email(email_aluno)

    # Pega todas as recompensas cadastradas
    recompensas = recompensa_dao.listar_todas()

    return render_template(
        "aluno/retirar_recompensas.html",
        aluno=aluno,
        recompensas=recompensas
    )
@aluno_bp.route('/comprar_recompensa', methods=['POST'])
def comprar_recompensa():
    if 'user' not in session or session.get('role') != 'aluno':
        return jsonify({"success": False, "message": "Faça login como aluno."})

    data = request.get_json()
    recomp_id = data.get("recompensa_id")
    aluno_email = session['user']

    recompensa = recompensa_dao.buscar_por_id(recomp_id)
    aluno = aluno_dao.buscar_por_email(aluno_email)

    if not recompensa or not aluno:
        return jsonify({"success": False, "message": "Recompensa ou aluno não encontrados."})

    if recompensa.vagas <= 0:
        return jsonify({"success": False, "message": "Essa recompensa já esgotou."})

    if aluno.saldo < recompensa.valor:
        return jsonify({"success": False, "message": "Saldo insuficiente."})

    try:
        # Atualiza saldo e vagas
        aluno.saldo -= recompensa.valor
        recompensa.vagas -= 1

        # Cria registro de resgate na MESMA sessão
        resgate = ResgateDB(
            aluno_email=aluno.email,
            recompensa_id=recompensa.id,
            valor_resgatado=recompensa.valor,
            status='pendente'
        )

        session_dao.add_all([aluno, recompensa, resgate])
        session_dao.commit()

        return jsonify({"success": True})
    except Exception as e:
        session_dao.rollback()
        return jsonify({"success": False, "message": str(e)})



@aluno_bp.route("/historico_resgates")
def historico_resgates():
    email = session.get('user')
    if not email or session.get('role') != 'aluno':
        flash("Faça login para acessar o histórico de resgates.")
        return redirect(url_for('login'))

    resgates = resgate_dao.listar_por_aluno(email)
    return render_template("aluno/historico_resgates.html", resgates=resgates)




@aluno_bp.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada.")
    return redirect(url_for('login'))