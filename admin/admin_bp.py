from flask import *
from database.database import *

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET', 'POST'])
def login_admin():
    print('tttt')
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == 'admin' and senha == '1234':
            session['admin_logado'] = True
            print("✅ Login bem-sucedido! Redirecionando para admin_dashboard...")
            return render_template('adm/admin.html')
        else:
            flash('Usuário ou senha incorretos!', 'erro')
    print(2)
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


@admin_bp.route('/detalharacao/<int:id>')
def mostrar_menu(id):
    return 'oi'


