from flask import *
from database.database import *
from models.modelosDB import *


avaliador_bp = admin_bp = Blueprint('avaliador', __name__, url_prefix='/avaliador')



@avaliador_bp.route('/avaliador', methods=['GET'])
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
    acoes = acao_realizadasDAO.listar_pendentes()
    print(len(acoes))
    return render_template('avaliador/avaliador.html')


@avaliador_bp.route('/aprovar/<int:id_acao>', methods=['POST'])
def aprovar_acao(id_acao):
    valor_ifcoins = int(request.form['valor'])
    acao_dao.aprovar_acao(id_acao, valor_ifcoins)
    flash("Ação aprovada com sucesso!")
    return redirect(url_for('avaliador_pagina'))

@avaliador_bp.route('/rejeitar/<int:id_acao>')
def rejeitar_acao(id_acao):
    acao_dao.rejeitar_acao(id_acao)
    flash("Ação rejeitada.")
    return redirect(url_for('avaliador_pagina'))