from flask import *
from database.database import *
from models.modelosDB import *

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'GET' and 'admin_logado' in session:
        return render_template('adm/admin.html')

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == 'admin' and senha == '1234': #criar DAO de blueprints/ model
            session['admin_logado'] = True
            return render_template('adm/admin.html')
        else:
            flash('Usuário ou senha incorretos!', 'erro')

    return render_template('adm/login_admin.html')


@admin_bp.route('/admin')
def admin_dashboard():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    return render_template('adm/admin.html')


@admin_bp.route('/logout')
def logout_admin():
    session.pop('admin_logado', None)
    flash('Logout realizado com sucesso!', 'sucesso')
    return render_template('adm/login_admin.html')


@admin_bp.route('/menuacoes')
def mostrar_menu():

    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    acoes = acao_dao.listar_todas()
    return render_template('adm/menuacoes.html', acoes=acoes)

@admin_bp.route('/cadastraracao', methods=['POST'])
def cadastrar_acao():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    nome = request.form.get('nome')
    valor = request.form.get('valor')
    descricao = request.form.get('descricao')

    nova_acao = AcaoDB(nome=nome, descricao=descricao, valor=valor)
    acao_dao.adicionar(nova_acao)

    return redirect(url_for('admin.mostrar_menu'))

@admin_bp.route('/editaracao/<int:id>', methods=['POST','GET'])
def editar_acao(id):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    if request.method == 'GET':
        acao = acao_dao.buscar_por_id(id)

        return render_template('adm/editaracao.html', acao=acao)

    nome = request.form.get('nome')
    valor = request.form.get('valor')
    descricao = request.form.get('descricao')

    if acao_dao.editar(AcaoDB(id=id, nome=nome, valor=valor, descricao=descricao)):
        return redirect(url_for('admin.mostrar_menu'))
    else:
        print('deu ruim. falta fazer a pagin html')
        return redirect(url_for('admin.mostrar_menu'))

@admin_bp.route('/excluiracao/<int:id_acao>')
def excluir_acao(id_acao):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    acao_dao.deletar(id_acao)
    return redirect(url_for('admin.mostrar_menu'))


@admin_bp.route('/avaliadorespendentes')
def listar_avaliadores_pendentes():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    avaliadores = avaliador_dao.listar_pendentes()
    return render_template('adm/avaliadorespendentes.html', avaliadores=avaliadores)


@admin_bp.route('/aprovar_avaliador/<email>')
def aprovar_avaliador(email):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    sucesso = avaliador_dao.aprovar_avaliador(email)
    if sucesso:
        flash(f"Avaliador {email} aprovado com sucesso!", "sucesso")
    else:
        flash("Erro ao aprovar avaliador.", "erro")

    return redirect(url_for('admin.listar_avaliadores_pendentes'))


@admin_bp.route('/rejeitar_avaliador/<email>')
def rejeitar_avaliador(email):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    sucesso = avaliador_dao.deletar(email)
    if sucesso:
        flash(f"Avaliador {email} rejeitado e removido do sistema.", "sucesso")
    else:
        flash("Avaliador não encontrado ou erro ao deletar.", "erro")

    return redirect(url_for('admin.listar_avaliadores_pendentes'))





