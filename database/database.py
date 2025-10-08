from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.pessoas import Base, AlunoDB, AvaliadorDB, AcaoDB

engine = create_engine('sqlite:///ifcoins.db')
Session = sessionmaker(bind=engine)
session = Session()

class AlunoDAO:
    def adicionar(self, aluno):
        session.add(aluno)
        session.commit()

    def buscar_por_email(self, email):
        return session.query(AlunoDB).filter_by(email=email).first()

    def obter_todos_alunos(self):
        return session.query(AlunoDB).all()

class AvaliadorDAO:
    def adicionar(self, avaliador):
        session.add(avaliador)
        session.commit()

    def buscar_por_email(self, email):
        return session.query(AvaliadorDB).filter_by(email=email).first()

    def listar_pendentes(self):
        return session.query(AvaliadorDB).filter_by(aprovado=False).all()

    def aprovar_avaliador(self, email):
        avaliador = self.buscar_por_email(email)
        if avaliador:
            avaliador.aprovado = True
            session.commit()

class AcaoDAO:
    def adicionar(self, acao):
        session.add(acao)
        session.commit()

    def listar_pendentes(self):
        return session.query(AcaoDB).filter_by(status='pendente').all()

    def listar_por_aluno(self, aluno_email):
        return session.query(AcaoDB).filter_by(aluno_email=aluno_email).all()

    def aprovar_acao(self, id_acao, valor):
        acao = session.query(AcaoDB).get(id_acao)
        if acao:
            acao.status = 'aprovada'
            acao.valor = valor
            aluno = session.query(AlunoDB).filter_by(email=acao.aluno_email).first()
            if aluno:
                aluno.saldo += valor
            session.commit()

    def rejeitar_acao(self, id_acao):
        acao = session.query(AcaoDB).get(id_acao)
        if acao:
            acao.status = 'rejeitada'
            session.commit()
