from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.modelosDAO import (
    AlunoDB, AvaliadorDB, AcaoDB, RecompensaDB, ResgateDB
)


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


# ============================================================
# 🔹 DAO: Avaliador
# ============================================================

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

    def listar_pendentes(self):
        # ⚠️ Só funciona se o modelo AcaoDB tiver o campo "status"
        return self.session.query(AcaoDB).filter_by(status='pendente').all()

    def listar_todas(self):
        return self.session.query(AcaoDB).all()

    def buscar_por_id(self, id_acao):
        return self.session.get(AcaoDB, id_acao)

    def aprovar_acao(self, acao_id):
        acao = self.buscar_por_id(acao_id)
        if acao and acao.status == 'pendente':
            acao.status = 'aprovada'
            aluno = acao.aluno
            aluno.saldo += acao.valor
            self.session.commit()
            return True
        return False

    def rejeitar_acao(self, acao_id):
        acao = self.buscar_por_id(acao_id)
        if acao and acao.status == 'pendente':
            acao.status = 'rejeitada'
            self.session.commit()
            return True
        return False



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
recompensa_dao = RecompensaDAO(session_dao)
resgate_dao = ResgateDAO(session_dao, recompensa_dao=recompensa_dao)
