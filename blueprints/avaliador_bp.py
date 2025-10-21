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
        print('a1')
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))
    print('a2')
    avaliador = avaliador_dao.buscar_por_email(email)
    if not avaliador.aprovado:
        print('a3')
        flash("Seu acesso ainda não foi aprovado pelo administrador.")
        return redirect(url_for('login'))
    print('a4')
    # Esta rota principal lista as ações PENDENTES (que também é o que 'acoesenviadas' lista)
    acoes = acao_realizadasDAO.listar_pendentes()
    print(len(acoes))
    return render_template('avaliador/avaliador.html', acoes=acoes)


# ROTA para listar ações DEFERIDAS (aprovadas)
@avaliador_bp.route('/acoes_deferidas', methods=['GET'])
def acoes_deferidas():
    email = session.get('user')
    role = session.get('role')
    if not email or role != 'avaliador':
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))

    acoes = acao_realizadasDAO.listar_deferidas() # Você precisa ter este método implementado
    return render_template('avaliador/acoes_deferidas.html', acoes=acoes)


# ROTA para listar ações ENVIADAS (Pendentes de avaliação)
# Esta rota é a mesma que a página inicial, mas pode ser útil para navegação.
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

    acao_realizadasDAO.aprovar_acao(id_acao)
    flash("Ação aprovada com sucesso!")
    return redirect(url_for('.avaliador_pagina')) # Use . para referenciar rotas dentro do Blueprint


@avaliador_bp.route('/rejeitar/<int:id_acao>')
def rejeitar_acao(id_acao):

    acao_realizadasDAO.rejeitar_acao(id_acao)
    flash("Ação rejeitada.")
    return redirect(url_for('.avaliador_pagina')) # Use . para referenciar rotas dentro do Blueprint


@avaliador_bp.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada.")
    return redirect(url_for('login'))