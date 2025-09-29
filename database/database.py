from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.pessoas import Base, AlunoDB, MestreDB, AcaoDB

engine = create_engine('sqlite:///ifcoins.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class AlunoDAO:
    def adicionar(self, aluno):
        session.add(aluno)
        session.commit()
    def buscar_por_email(self, email):
        return session.query(AlunoDB).filter_by(email=email).first()

class MestreDAO:
    def adicionar(self, mestre):
        session.add(mestre)
        session.commit()
    def buscar_por_email(self, email):
        return session.query(MestreDB).filter_by(email=email).first()
    def listar_pendentes(self):
        return session.query(MestreDB).filter_by(aprovado=False).all()
    def aprovar_mestre(self, email):
        mestre = self.buscar_por_email(email)
        if mestre:
            mestre.aprovado = True
            session.commit()

class AcaoDAO:
    def adicionar(self, acao):
        session.add(acao)
        session.commit()
    def listar_pendentes(self):
        return session.query(AcaoDB).filter_by(status='pendente').all()
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
