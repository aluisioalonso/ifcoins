from flask import *
from database.database import *
from models.modelosDB import *

# O Blueprint é definido aqui.
avaliador_bp = Blueprint('avaliador', __name__, url_prefix='/avaliador')
# Lembre-se de que os DAOs (avaliador_dao, acao_realizadasDAO, acao_dao)
# precisam estar definidos e importados de 'database.database'.


@avaliador_bp.route('/', methods=['GET'])
def avaliador_pagina():
    email = session.get('user')
    role = session.get('role')

    if not email or role != 'avaliador':
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))

    avaliador = avaliador_dao.buscar_por_email(email)

    if avaliador is None:
        flash("Avaliador não encontrado no sistema. Verifique seu login.")
        return redirect(url_for('login'))

    if avaliador.status != 'aprovado':
        flash("Seu acesso ainda não foi aprovado pelo administrador.")
        return redirect(url_for('login'))

    acoes = acao_realizadasDAO.listar_pendentes()
    return render_template('avaliador/avaliador.html', acoes=acoes)


@avaliador_bp.route('/acoes_deferidas', methods=['GET'])
def acoes_deferidas():
    email = session.get('user')
    role = session.get('role')
    if not email or role != 'avaliador':
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))

    # LISTA TODAS AS AÇÕES APROVADAS/REJEITADAS
    acoes_aprovadas = acao_realizadasDAO.listar_todas_aprovadas()
    acoes_rejeitadas = acao_realizadasDAO.listar_todas_rejeitadas()

    return render_template(
        'avaliador/acoes_deferidas.html',
        acoes_aprovadas=acoes_aprovadas,
        acoes_rejeitadas=acoes_rejeitadas
    )





@avaliador_bp.route('/acoesenviadas', methods=['GET'])
def acoes_enviadas():
    email = session.get('user')
    role = session.get('role')
    if not email or role != 'avaliador':
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))

    acoes = acao_realizadasDAO.listar_pendentes() # Listar ações pendentes
    return render_template('avaliador/acoes_enviadas.html', acoes=acoes)



@avaliador_bp.route('/aprovar/<int:id_acao>')
def aprovar_acao(id_acao):
    email = session.get('user')
    role = session.get('role')

    if not email or role != 'avaliador':
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))

    avaliador = avaliador_dao.buscar_por_email(email)
    acao = acao_realizadasDAO.buscar_por_id(id_acao)

    if acao.email_aluno == avaliador.email:
        flash(" Você não pode aprovar uma ação que você mesmo enviou.", "erro")
        return redirect(url_for('.acoes_enviadas'))

    acao_realizadasDAO.aprovar_acao(id_acao)
    flash("✅ Ação aprovada com sucesso!", "sucesso")
    return redirect(url_for('.avaliador_pagina'))


@avaliador_bp.route('/rejeitar/<int:id_acao>')
def rejeitar_acao(id_acao):
    email = session.get('user')
    role = session.get('role')

    if not email or role != 'avaliador':
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))

    avaliador = avaliador_dao.buscar_por_email(email)
    acao = acao_realizadasDAO.buscar_por_id(id_acao)

    if acao.email_aluno == avaliador.email:
        flash("Você não pode rejeitar uma ação que você mesmo enviou.", "erro")
        return redirect(url_for('.acoes_enviadas'))

    acao_realizadasDAO.rejeitar_acao(id_acao)
    flash(" Ação rejeitada com sucesso.", "sucesso")
    return redirect(url_for('.avaliador_pagina'))


@avaliador_bp.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada.")
    return redirect(url_for('login'))

