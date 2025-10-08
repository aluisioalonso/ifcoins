from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.database import AlunoDAO, AvaliadorDAO, AcaoDAO, session as db_session
from models.pessoas import AlunoDB, AvaliadorDB, AcaoDB

app = Flask(__name__)
app.secret_key = 'IUY$#YIy5i#5232'

aluno_dao = AlunoDAO()
avaliador_dao = AvaliadorDAO()
acao_dao = AcaoDAO()



@app.route("/compras_disponiveis")
def compras_disponiveis():
    return render_template("compras_disponiveis.html")


@app.route("/historico_acoes")
def historico_acoes():
    return "<h1>Histórico de ações</h1>"


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        role = request.form.get('role')
        email_domain = '@academico.ifpb.edu.br'
        email = email + email_domain

        if role == 'aluno':
            user = aluno_dao.buscar_por_email(email)
        else:
            user = avaliador_dao.buscar_por_email(email)

        if user and user.senha == senha and role == 'aluno':
            session['user'] = user.email
            session['role'] = 'aluno'
            return redirect(url_for('aluno_pagina'))
        elif user and user.senha == senha and role == 'avaliador':
            if not user.aprovado:
                flash("Seu acesso ainda não foi aprovado pelo administrador.")
                return redirect(url_for('login'))
            session['user'] = user.email
            session['role'] = 'avaliador'
            return redirect(url_for('avaliador_pagina'))
        else:
            flash("Email ou senha incorretos.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/cadastrousuario', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        role = request.form['role']
        email_user = request.form['emailUser']
        senha = request.form['senha']
        email_domain = '@academico.ifpb.edu.br'
        email = email_user + email_domain

        if role == 'aluno':
            aluno = AlunoDB(nome=nome, email=email, senha=senha, saldo=0)
            aluno_dao.adicionar(aluno)
        elif role == 'avaliador':
            avaliador = AvaliadorDB(nome=nome, email=email, senha=senha, aprovado=False)
            avaliador_dao.adicionar(avaliador)
            flash("Seu login foi solicitado com sucesso")

        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/aluno', methods=['GET', 'POST'])
def aluno_pagina():
    email = session.get('user')
    role = session.get('role')
    if not email or role != 'aluno':
        flash("Faça login para acessar a página do aluno.")
        return redirect(url_for('login'))

    aluno = aluno_dao.buscar_por_email(email)
    acoes_aluno = acao_dao.listar_por_aluno(email)

    if request.method == 'POST':
        descricao = request.form['descricao']
        nova_acao = AcaoDB(descricao=descricao, aluno_email=aluno.email, status='pendente', valor=0)
        acao_dao.adicionar(nova_acao)
        flash(f"Ação '{descricao}' enviada para aprovação do avaliador!")
        return redirect(url_for('aluno_pagina'))

    return render_template('aluno.html', aluno=aluno, acoes_disponiveis=acoes_aluno)

@app.route('/avaliador', methods=['GET'])
def avaliador_pagina():
    email = session.get('user')
    role = session.get('role')
    if not email or role != 'avaliador':
        flash("Faça login como avaliador para acessar esta página.")
        return redirect(url_for('login'))

    avaliador = avaliador_dao.buscar_por_email(email)
    if not avaliador.aprovado:
        flash("Seu acesso ainda não foi aprovado pelo administrador.")
        return redirect(url_for('login'))

    acoes = acao_dao.listar_pendentes()
    return render_template('avaliador.html', acoes=acoes, acoes_disponiveis=acoes_disponiveis)

@app.route('/aprovar/<int:id_acao>', methods=['POST'])
def aprovar_acao(id_acao):
    valor_ifcoins = int(request.form['valor'])
    acao_dao.aprovar_acao(id_acao, valor_ifcoins)
    flash("Ação aprovada com sucesso!")
    return redirect(url_for('avaliador_pagina'))

@app.route('/rejeitar/<int:id_acao>')
def rejeitar_acao(id_acao):
    acao_dao.rejeitar_acao(id_acao)
    flash("Ação rejeitada.")
    return redirect(url_for('avaliador_pagina'))

@app.route('/admin')
def admin():
    avaliadores_pendentes = avaliador_dao.listar_pendentes()
    return render_template('admin.html', avaliadores=avaliadores_pendentes)

@app.route('/aprovar_avaliador/<email>')
def aprovar_avaliador(email):
    avaliador_dao.aprovar_avaliador(email)
    flash(f"Avaliador {email} aprovado!")
    return redirect(url_for('admin'))

@app.route('/rejeitar_avaliador/<email>')
def rejeitar_avaliador(email):
    avaliador = avaliador_dao.buscar_por_email(email)
    if avaliador:
        db_session.delete(avaliador)
        db_session.commit()
        flash(f"Avaliador {email} rejeitado e removido do sistema.")
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
