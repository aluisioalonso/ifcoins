from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.database import AlunoDAO, MestreDAO, AcaoDAO, session as db_session
from models.pessoas import AlunoDB, MestreDB, AcaoDB

app = Flask(__name__)
app.secret_key = 'supersecretkey'

aluno_dao = AlunoDAO()
mestre_dao = MestreDAO()
acao_dao = AcaoDAO()

acoes_disponiveis = {
    "Deu bom dia": 20,
    "Salvou um animal": 100,
    "Ajudou colega": 50,
    "Organizou mural": 30
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        role = request.form.get('role')
        if role == 'aluno':
            user = aluno_dao.buscar_por_email(email)
        else:
            user = mestre_dao.buscar_por_email(email)
        if user and user.senha == senha and role == 'aluno':
            session['user'] = user.email
            session['role'] = 'aluno'
            return redirect(url_for('aluno_pagina'))
        elif user and user.senha == senha and role == 'mestre':
            if not user.aprovado:
                flash("Seu acesso ainda não foi aprovado pelo administrador.")
                return redirect(url_for('login'))
            session['user'] = user.email
            session['role'] = 'mestre'
            return redirect(url_for('mestre_pagina'))
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
        email_domain = '@ifpb.edu.br' if role == 'mestre' else '@academico.ifpb.edu.br'
        email = email_user + email_domain

        if role == 'aluno':
            aluno = AlunoDB(nome=nome, email=email, senha=senha)
            aluno_dao.adicionar(aluno)
        elif role == 'mestre':
            mestre = MestreDB(nome=nome, email=email, senha=senha, aprovado=False)
            mestre_dao.adicionar(mestre)
            flash("Seu login foi solicitado com sucesso")

        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/aluno', methods=['GET', 'POST'])
def aluno_pagina():
    email = session.get('aluno_email')
    if not email:
        flash("Faça login para acessar a página do aluno.")
        return redirect(url_for('login'))
    aluno = aluno_dao.buscar_por_email(email)
    if request.method == 'POST':
        descricao = request.form['descricao']
        nova_acao = AcaoDB(descricao=descricao, aluno_email=aluno.email, status='pendente', valor=0)
        acao_dao.adicionar(nova_acao)
        flash(f"Ação '{descricao}' enviada para aprovação do mestre!")
        return redirect(url_for('aluno_pagina'))
    return render_template('aluno.html', aluno=aluno, acoes_disponiveis=acoes_disponiveis)

@app.route('/mestre', methods=['GET'])
def mestre_pagina():
    email = session.get('mestre_email')
    if not email:
        flash("Faça login como mestre para acessar esta página.")
        return redirect(url_for('login'))
    mestre = mestre_dao.buscar_por_email(email)
    if not mestre.aprovado:
        flash("Seu acesso ainda não foi aprovado pelo administrador.")
        return redirect(url_for('login'))
    acoes = acao_dao.listar_pendentes()
    return render_template('mestre.html', acoes=acoes, acoes_disponiveis=acoes_disponiveis)

@app.route('/aprovar/<int:id_acao>', methods=['POST'])
def aprovar_acao(id_acao):
    valor_ifcoins = int(request.form['valor'])
    acao_dao.aprovar_acao(id_acao, valor_ifcoins)
    flash("Ação aprovada com sucesso!")
    return redirect(url_for('mestre_pagina'))

@app.route('/rejeitar/<int:id_acao>')
def rejeitar_acao(id_acao):
    acao_dao.rejeitar_acao(id_acao)
    flash("Ação rejeitada.")
    return redirect(url_for('mestre_pagina'))

@app.route('/admin')
def admin():
    mestres_pendentes = mestre_dao.listar_pendentes()
    return render_template('admin.html', mestres=mestres_pendentes)

@app.route('/aprovar_mestre/<email>')
def aprovar_mestre(email):
    mestre_dao.aprovar_mestre(email)
    flash(f"Mestre {email} aprovado!")
    return redirect(url_for('admin'))

@app.route('/rejeitar_mestre/<email>')
def rejeitar_mestre(email):
    mestre = mestre_dao.buscar_por_email(email)
    if mestre:
        db_session.delete(mestre)
        db_session.commit()
        flash(f"Mestre {email} rejeitado e removido do sistema.")
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
