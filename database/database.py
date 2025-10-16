from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.modelosDB import (
    AlunoDB, AvaliadorDB, AcaoDB, RecompensaDB, ResgateDB
)
from models.modelosDB import AcaoRealizadaAlunoDB, AlunoDB, AcaoDB
from datetime import datetime


engine = create_engine('sqlite:///ifcoins.db', echo=False)
Session = sessionmaker(bind=engine)
session_dao = Session()


class AlunoDAO:
    def __init__(self, session):
        self.session = session

    def adicionar(self, aluno):
        self.session.add(aluno)
        self.session.commit()

    def buscar_por_email(self, email):
        return self.session.query(AlunoDB).filter_by(email=email).first()

    def obter_todos_alunos(self):
        return self.session.query(AlunoDB).all()


class AvaliadorDAO:
    def __init__(self, session):
        self.session = session

    def adicionar(self, avaliador):
        self.session.add(avaliador)
        self.session.commit()

    def buscar_por_email(self, email):
        return self.session.query(AvaliadorDB).filter_by(email=email).first()

    def listar_pendentes(self):
        return self.session.query(AvaliadorDB).filter_by(aprovado=False).all()

    def aprovar_avaliador(self, email):
        avaliador = self.buscar_por_email(email)
        if avaliador:
            avaliador.aprovado = True
            self.session.commit()
            return True
        return False


class AcaoDAO:
    def __init__(self, session):
        self.session = session

    def adicionar(self, acao):
        self.session.add(acao)
        self.session.commit()

    def editar(self, acao):
        self.session.merge(acao)
        self.session.commit()
        return True

    def deletar(self, id):
        try:
            acao = acao_dao.buscar_por_id(id)
            if not acao:
                return False

            session_dao.delete(acao)
            session_dao.commit()
            return True
        except Exception as e:
            session_dao.rollback()
            return False

    def listar_todas(self):
        return self.session.query(AcaoDB).all()

    def buscar_por_id(self, id_acao):
        return self.session.get(AcaoDB, id_acao)


class AcaoRealizadaDAO:
    def __init__(self, session, aluno_dao=None, acao_dao=None):
        self.session = session
        self.aluno_dao = aluno_dao
        self.acao_dao = acao_dao

    def adicionar(self, acao_realizada):
        self.session.add(acao_realizada)
        self.session.commit()

    def listar_pendentes(self):
        return self.session.query(AcaoRealizadaAlunoDB).filter_by(status='pendente').all()

    def listar_todas(self):
        return self.session.query(AcaoRealizadaAlunoDB).all()

    def buscar_por_id(self, id_acao_realizada):
        return self.session.get(AcaoRealizadaAlunoDB, id_acao_realizada)

    def listar_por_aluno(self, email_aluno):
        return (
            self.session.query(AcaoRealizadaAlunoDB)
            .filter_by(email_aluno=email_aluno)
            .order_by(AcaoRealizadaAlunoDB.data_envio.desc())
            .all()
        )

    def processar_acao(self, id_acao_realizada, status, valor=0, comentario=None):
        acao_realizada = self.buscar_por_id(id_acao_realizada)
        if not acao_realizada:
            return False, "Ação não encontrada."

        if status not in ['aprovada', 'rejeitada']:
            return False, "Status inválido."

        aluno = self.session.query(AlunoDB).filter_by(email=acao_realizada.email_aluno).first()
        if not aluno:
            return False, "Aluno não encontrado."

        try:
            acao_realizada.status = status
            if comentario:
                acao_realizada.comentarios_aluno = comentario

            if status == 'aprovada':
                acao_realizada.valor = valor
                aluno.saldo += valor

            self.session.commit()
            return True, f"Ação {status} com sucesso!"

        except Exception as e:
            self.session.rollback()
            return False, f"Erro ao processar ação: {e}"

    def excluir(self, id_acao_realizada):
        acao_realizada = self.buscar_por_id(id_acao_realizada)
        if not acao_realizada:
            return False
        self.session.delete(acao_realizada)
        self.session.commit()
        return True


class RecompensaDAO:
    def __init__(self, session):
        self.session = session

    def adicionar(self, recompensa):
        self.session.add(recompensa)
        self.session.commit()

    def buscar_por_id(self, id_recompensa):
        return self.session.get(RecompensaDB, id_recompensa)

    def listar_disponiveis(self):
        return (
            self.session.query(RecompensaDB)
            .filter(RecompensaDB.estoque > 0, RecompensaDB.custo > 0)
            .all()
        )

    def listar_todas(self):
        return self.session.query(RecompensaDB).all()


class ResgateDAO:
    def __init__(self, session, recompensa_dao=None):
        self.session = session
        self.recompensa_dao = recompensa_dao  # 👈 injeta dependência

    def adicionar(self, resgate):
        self.session.add(resgate)
        self.session.commit()

    def listar_pendentes(self):
        return self.session.query(ResgateDB).filter_by(status='pendente').all()

    def buscar_por_id(self, id_resgate):
        return self.session.get(ResgateDB, id_resgate)

    def processar_resgate(self, id_resgate, status):
        resgate = self.buscar_por_id(id_resgate)
        if resgate:
            resgate.status = status
            self.session.commit()
            return True
        return False

    def resgatar_recompensa(self, aluno_email, recompensa_id):
        aluno = self.session.query(AlunoDB).filter_by(email=aluno_email).one()
        recompensa = self.recompensa_dao.buscar_por_id(recompensa_id)

        if not recompensa:
            return False, "Recompensa não encontrada."

        if recompensa.estoque <= 0:
            return False, "Sem estoque disponível."

        if aluno.saldo < recompensa.custo:
            return False, "Saldo insuficiente."

        try:
            aluno.saldo -= recompensa.custo
            recompensa.estoque -= 1

            novo_resgate = ResgateDB(
                aluno_email=aluno_email,
                recompensa_id=recompensa_id,
                valor_resgatado=recompensa.custo,
                status='pendente'
            )
            self.session.add(novo_resgate)
            self.session.commit()
            return True, "Resgate solicitado com sucesso!"

        except Exception as e:
            self.session.rollback()
            return False, f"Erro ao processar resgate: {e}"


aluno_dao = AlunoDAO(session_dao)
avaliador_dao = AvaliadorDAO(session_dao)
acao_dao = AcaoDAO(session_dao)
acao_realizadasDAO = AcaoRealizadaDAO(session_dao)
recompensa_dao = RecompensaDAO(session_dao)
resgate_dao = ResgateDAO(session_dao, recompensa_dao=recompensa_dao)
