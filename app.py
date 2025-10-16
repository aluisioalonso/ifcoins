from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.modelosDB import AlunoDB, AvaliadorDB
from blueprints.admin_bp import admin_bp
from blueprints.avaliador_bp import avaliador_bp
from database.database import (
    aluno_dao, avaliador_dao , )

app = Flask(__name__)
app.secret_key = 'IUY$#YIy5i#5232'
EMAIL_DOMAIN = '@academico.ifpb.edu.br'

app.register_blueprint(admin_bp)
app.register_blueprint(avaliador_bp)

@app.route('/adm/logout')
def logout_admin():
    session.pop('admin_logado', None)
    flash('Logout realizado com sucesso!', 'sucesso')
    return redirect(url_for('login_admin'))


@app.route("/compras_disponiveis")
def compras_disponiveis():
    return render_template("aluno/compras_disponiveis.html")


@app.route("/historico_acoes")
def historico_acoes():
    return "<h1>Histórico de ações</h1>"



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_input = request.form['email']
        senha = request.form['senha']
        role = request.form.get('role')#aluno ou avaliador
        email = email_input + EMAIL_DOMAIN

        if role == 'aluno':
            user = aluno_dao.buscar_por_email(email)
        else:
            user = avaliador_dao .buscar_por_email(email)

        if user and user.senha == senha and role == 'aluno':

            session['user'] = user.email
            session['role'] = 'aluno'
            return redirect(url_for('aluno_pagina'))
        elif user and user.senha == senha and role == 'avaliador':
            print('avaliador:', email, senha)
            if not user.aprovado:
                flash("Seu acesso ainda não foi aprovado pelo administrador.")
                return redirect(url_for('login'))
            session['user'] = user.email
            session['role'] = 'avaliador'
            return redirect(url_for('avaliador.avaliador_pagina'))
        else:
            flash("Email ou senha incorretos.")
            print('senha ou email errados')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada.")
    return redirect(url_for('login'))

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
            if aluno_dao.buscar_por_email(email):
                flash("Este e-mail de aluno já está cadastrado.", 'error')
                return redirect(url_for('cadastro'))
            aluno = AlunoDB(nome=nome, email=email, senha=senha, saldo=0)
            aluno_dao.adicionar(aluno)
        elif role == 'avaliador':
            print('entrou p cadastrar avaliador')
            print(nome, email, senha)
            if avaliador_dao .buscar_por_email(email):
                flash("Este e-mail de avaliador já está cadastrado.", 'error')
                return redirect(url_for('cadastro'))
            avaliador = AvaliadorDB(nome=nome, email=email, senha=senha, aprovado=False)
            avaliador_dao.adicionar(avaliador)
            print('cadastrado com sucesso avaliador')
            flash("Seu login foi solicitado com sucesso. Aguarde aprovação.")

        return redirect(url_for('login'))
    return render_template('cadastro.html')


@app.route('/aluno', methods=['GET', 'POST'])
def aluno_pagina():
    email = session.get('user')
    if not email or session.get('role') != 'aluno':
        flash("Faça login para acessar a página do aluno.")
        return redirect(url_for('login'))

    aluno = aluno_dao.buscar_por_email(email)
    # Corrigido para usar a lista de acoes reais
    #acoes_aluno = acao_dao.listar_por_aluno(email)

    '''
        if request.method == 'POST':
        descricao = request.form['descricao']

        nova_acao = AcaoDB(
            descricao=descricao,
            aluno_email=aluno.email,
            status='pendente',
            valor=0
        )
        acao_dao.adicionar(nova_acao)
        flash(f"Ação '{descricao}' enviada para aprovação do avaliador!")
        return redirect(url_for('aluno_pagina'))

    '''

    return render_template('aluno/aluno.html', aluno=aluno)








if __name__ == '__main__':
    app.run(debug=True, port=5002)