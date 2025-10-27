from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from database.database import *
from models.modelosDB import *
from database.database import admin_dao  # ✅ novo DAO
from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET', 'POST'])
def login_admin():
    """Página de login do administrador"""
    if request.method == 'GET' and 'admin_logado' in session:
        return render_template('adm/admin.html')

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        # ✅ Validação via DAO
        if admin_dao.validar_login(usuario, senha):
            session['admin_logado'] = True
            session['admin_usuario'] = usuario
            flash('Login realizado com sucesso!', 'sucesso')
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
    session.pop('admin_usuario', None)
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


@admin_bp.route('/editaracao/<int:id>', methods=['POST', 'GET'])
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
        flash('Erro ao editar ação.', 'erro')
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


@admin_bp.route('/buscaravaliador', methods=['GET'])
def buscar_avaliador():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    termo_busca = request.args.get('q', '').strip()
    filtro = request.args.get('filtro', '').strip()

    if not termo_busca:
        avaliadores = avaliador_dao.listar_todos()
    else:
        query = session_dao.query(AvaliadorDB)
        if filtro == 'email':
            avaliadores = query.filter(AvaliadorDB.email.ilike(f"%{termo_busca}%")).all()
        else:
            avaliadores = query.filter(AvaliadorDB.nome.ilike(f"%{termo_busca}%")).all()

    return render_template('adm/buscar_avaliador.html', avaliadores=avaliadores, termo=termo_busca, filtro=filtro)


@admin_bp.route('/remover_avaliador/<email>', methods=['DELETE', 'POST'])
def remover_avaliador(email):
    if 'admin_logado' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    sucesso = avaliador_dao.deletar(email)
    if sucesso:
        return jsonify({'mensagem': f"Avaliador {email} removido com sucesso!"}), 200
    else:
        return jsonify({'erro': 'Falha ao remover avaliador.'}), 400



@admin_bp.route('/menurecompensas')
def mostrar_recompensas():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    recompensas = recompensa_dao.listar_todas()
    return render_template('adm/menu_recompensas.html', recompensas=recompensas)


@admin_bp.route('/cadastrarrecompensa', methods=['POST'])
def cadastrar_recompensa():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    tipo = request.form.get('tipo')
    descricao = request.form.get('descricao')
    valor = request.form.get('valor', type=float)
    link = request.form.get('link')
    vagas = request.form.get('vagas', type=int)
    data_expiracao = request.form.get('data_expiracao')
    if data_expiracao:
        data_expiracao = datetime.strptime(data_expiracao, '%Y-%m-%d')

    nova_recompensa = RecompensaDB(
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        link=link,
        vagas=vagas,
        data_expiracao=data_expiracao
    )
    recompensa_dao.adicionar(nova_recompensa)
    flash(f'Recompensa "{tipo}" cadastrada com sucesso!', 'sucesso')
    return redirect(url_for('admin.mostrar_recompensas'))


@admin_bp.route('/editarrecompensa/<int:id>', methods=['POST'])
def editar_recompensa(id):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    tipo = request.form.get('tipo')
    descricao = request.form.get('descricao')
    valor = request.form.get('valor', type=float)
    link = request.form.get('link')
    vagas = request.form.get('vagas', type=int)
    data_expiracao = request.form.get('data_expiracao')
    if data_expiracao:
        data_expiracao = datetime.strptime(data_expiracao, '%Y-%m-%d')

    sucesso = recompensa_dao.editar(RecompensaDB(
        id=id,
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        link=link,
        vagas=vagas,
        data_expiracao=data_expiracao
    ))
    if sucesso:
        flash(f'Recompensa "{tipo}" editada com sucesso!', 'sucesso')
    else:
        flash('Erro ao editar recompensa.', 'erro')
    return redirect(url_for('admin.mostrar_recompensas'))



@admin_bp.route('/excluirrecompensa/<int:id>')
def excluir_recompensa(id):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    sucesso = recompensa_dao.deletar(id)
    if sucesso:
        flash('Recompensa excluída com sucesso!', 'sucesso')
    else:
        flash('Erro ao excluir recompensa.', 'erro')
    return redirect(url_for('admin.mostrar_recompensas'))
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from database.database import *
from models.modelosDB import *
from database.database import admin_dao  # ✅ novo DAO
from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET', 'POST'])
def login_admin():
    """Página de login do administrador"""
    if request.method == 'GET' and 'admin_logado' in session:
        return render_template('adm/admin.html')

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        # ✅ Validação via DAO
        if admin_dao.validar_login(usuario, senha):
            session['admin_logado'] = True
            session['admin_usuario'] = usuario
            flash('Login realizado com sucesso!', 'sucesso')
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
    session.pop('admin_usuario', None)
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


@admin_bp.route('/editaracao/<int:id>', methods=['POST', 'GET'])
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
        flash('Erro ao editar ação.', 'erro')
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


@admin_bp.route('/buscaravaliador', methods=['GET'])
def buscar_avaliador():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    termo_busca = request.args.get('q', '').strip()
    filtro = request.args.get('filtro', '').strip()

    if not termo_busca:
        avaliadores = avaliador_dao.listar_todos()
    else:
        avaliadores = avaliador_dao.buscar(termo_busca, filtro)

    return render_template('adm/buscar_avaliador.html',
                           avaliadores=avaliadores,
                           termo=termo_busca,
                           filtro=filtro)



@admin_bp.route('/remover_avaliador/<email>', methods=['DELETE', 'POST'])
def remover_avaliador(email):
    if 'admin_logado' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    sucesso = avaliador_dao.deletar(email)
    if sucesso:
        return jsonify({'mensagem': f"Avaliador {email} removido com sucesso!"}), 200
    else:
        return jsonify({'erro': 'Falha ao remover avaliador.'}), 400



@admin_bp.route('/menurecompensas')
def mostrar_recompensas():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    recompensas = recompensa_dao.listar_todas()
    return render_template('adm/menu_recompensas.html', recompensas=recompensas)


@admin_bp.route('/cadastrarrecompensa', methods=['POST'])
def cadastrar_recompensa():
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    tipo = request.form.get('tipo')
    descricao = request.form.get('descricao')
    valor = request.form.get('valor', type=float)
    link = request.form.get('link')
    vagas = request.form.get('vagas', type=int)
    data_expiracao = request.form.get('data_expiracao')
    if data_expiracao:
        data_expiracao = datetime.strptime(data_expiracao, '%Y-%m-%d')

    nova_recompensa = RecompensaDB(
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        link=link,
        vagas=vagas,
        data_expiracao=data_expiracao
    )
    recompensa_dao.adicionar(nova_recompensa)
    flash(f'Recompensa "{tipo}" cadastrada com sucesso!', 'sucesso')
    return redirect(url_for('admin.mostrar_recompensas'))


@admin_bp.route('/editarrecompensa/<int:id>', methods=['POST'])
def editar_recompensa(id):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    tipo = request.form.get('tipo')
    descricao = request.form.get('descricao')
    valor = request.form.get('valor', type=float)
    link = request.form.get('link')
    vagas = request.form.get('vagas', type=int)
    data_expiracao = request.form.get('data_expiracao')
    if data_expiracao:
        data_expiracao = datetime.strptime(data_expiracao, '%Y-%m-%d')

    sucesso = recompensa_dao.editar(RecompensaDB(
        id=id,
        tipo=tipo,
        descricao=descricao,
        valor=valor,
        link=link,
        vagas=vagas,
        data_expiracao=data_expiracao
    ))
    if sucesso:
        flash(f'Recompensa "{tipo}" editada com sucesso!', 'sucesso')
    else:
        flash('Erro ao editar recompensa.', 'erro')
    return redirect(url_for('admin.mostrar_recompensas'))



@admin_bp.route('/excluirrecompensa/<int:id>')
def excluir_recompensa(id):
    if 'admin_logado' not in session:
        return render_template('adm/login_admin.html')

    sucesso = recompensa_dao.deletar(id)
    if sucesso:
        flash('Recompensa excluída com sucesso!', 'sucesso')
    else:
        flash('Erro ao excluir recompensa.', 'erro')
    return redirect(url_for('admin.mostrar_recompensas'))


@admin_bp.route("/buscaraluno")
def listar_alunos():
    q = request.args.get("q", "")
    if q:
        alunos = [a for a in aluno_dao.obter_todos_alunos() if q.lower() in a.nome.lower() or q.lower() in a.email.lower()]
    else:
        alunos = aluno_dao.obter_todos_alunos()
    return render_template("adm/buscaralunos.html", alunos=alunos)

@admin_bp.route("/remover_aluno/<email>", methods=["DELETE", "POST"])
def remover_aluno(email):
    aluno = aluno_dao.buscar_por_email(email)
    if aluno:
        aluno_dao.session.delete(aluno)
        aluno_dao.session.commit()
        return {"success": True}, 200
    return {"error": "Aluno não encontrado"}, 404
