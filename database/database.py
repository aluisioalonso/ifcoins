from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,joinedload
from werkzeug.security import check_password_hash
from models.modelosDB import (
    AlunoDB, AvaliadorDB, AcaoDB, RecompensaDB, ResgateDB, AcaoRealizadaAlunoDB, AdminDB, Base
)
from datetime import datetime


engine = create_engine(
    'postgresql+psycopg2://adminifcoins:GrandTheftAuto.30/10/2004@localhost:5432/ifcoins',
    echo=False
)

Session = sessionmaker(bind=engine)
session_dao = Session()
Base.metadata.create_all(engine)


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
        return self.session.query(AvaliadorDB).filter_by(status='pendente').all()

    def listar_aprovados(self):
        return self.session.query(AvaliadorDB).filter_by(status='aprovado').all()

    def listar_rejeitados(self):
        return self.session.query(AvaliadorDB).filter_by(status='rejeitado').all()

    def listar_todos(self):
        return self.session.query(AvaliadorDB).all()

    def aprovar_avaliador(self, email):
        avaliador = self.buscar_por_email(email)
        if avaliador:
            avaliador.status = 'aprovado'
            self.session.commit()
            return True
        return False

    def rejeitar_avaliador(self, email):
        avaliador = self.buscar_por_email(email)
        if avaliador:
            avaliador.status = 'rejeitado'
            self.session.commit()
            return True
        return False

    def buscar(self, termo_busca, filtro=None):
        termo = f"%{termo_busca.strip()}%"
        query = self.session.query(AvaliadorDB)

        if filtro == "email":
            return query.filter(AvaliadorDB.email.ilike(termo)).all()
        else:
            return query.filter(AvaliadorDB.nome.ilike(termo)).all()

    def deletar(self, email):
        avaliador = self.buscar_por_email(email)
        if not avaliador:
            return False
        try:
            self.session.delete(avaliador)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
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
            acao = self.buscar_por_id(id)
            if not acao:
                return False
            self.session.delete(acao)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
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

    def listar_todas(self):
        return self.session.query(AcaoRealizadaAlunoDB).all()

    def listar_pendentes(self):
        return self.session.query(AcaoRealizadaAlunoDB).filter_by(status='pendente').all()


    def listar_aprovadas_por_aluno(self, email_aluno):
        return self.session.query(AcaoRealizadaAlunoDB)\
            .filter_by(status='aprovado', email_aluno=email_aluno).all()

    # Listar ações rejeitadas de um aluno específico
    def listar_rejeitadas_por_aluno(self, email_aluno):
        return self.session.query(AcaoRealizadaAlunoDB)\
            .filter_by(status='rejeitado', email_aluno=email_aluno).all()

    def listar_todas_aprovadas(self):
        return self.session.query(AcaoRealizadaAlunoDB).filter_by(status='aprovado').all()

    def listar_todas_rejeitadas(self):
        return self.session.query(AcaoRealizadaAlunoDB).filter_by(status='rejeitado').all()

    def listar_pendentes_por_aluno(self, email_aluno):
        return self.session.query(AcaoRealizadaAlunoDB) \
            .filter_by(status='pendente', email_aluno=email_aluno).all()

    def buscar_por_id(self, id_acao_realizada):
        return self.session.get(AcaoRealizadaAlunoDB, id_acao_realizada)

    def aprovar_acao(self, id_acao_realizada, comentario=None):
        acao_realizada = self.buscar_por_id(id_acao_realizada)
        if not acao_realizada:
            return False, "Ação não encontrada."

        if acao_realizada.status == 'aprovado':
            return False, "Ação já aprovada."

        aluno = self.session.query(AlunoDB).filter_by(email=acao_realizada.email_aluno).first()
        if not aluno:
            return False, "Aluno não encontrado."

        try:
            acao_realizada.status = 'aprovado'
            if comentario:
                acao_realizada.comentarios_aluno = comentario

            aluno.saldo += acao_realizada.valor
            self.session.commit()
            return True, "Ação aprovada com sucesso!"
        except Exception as e:
            self.session.rollback()
            return False, f"Erro ao aprovar ação: {e}"

    def rejeitar_acao(self, id_acao_realizada):
        acao_realizada = self.buscar_por_id(id_acao_realizada)
        if not acao_realizada:
            return False, "Ação não encontrada."

        if acao_realizada.status == 'rejeitado':
            return False, "Ação já rejeitada."

        try:
            acao_realizada.status = 'rejeitado'
            self.session.commit()
            return True, "Ação rejeitada com sucesso!"
        except Exception as e:
            self.session.rollback()
            return False, f"Erro ao rejeitar ação: {e}"



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

    def editar(self, recompensa):
        try:
            self.session.merge(recompensa)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    def deletar(self, id_recompensa):
        try:
            recompensa = self.buscar_por_id(id_recompensa)
            if not recompensa:
                return False
            self.session.delete(recompensa)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()


class ResgateDAO:
    def __init__(self, session, recompensa_dao=None):
        self.session = session
        self.recompensa_dao = recompensa_dao

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

    def listar_por_aluno(self, aluno_email):
        return (
            self.session.query(ResgateDB)
            .options(joinedload(ResgateDB.recompensa))
            .filter_by(aluno_email=aluno_email)
            .order_by(ResgateDB.data_resgate.desc())
            .all()
        )

class AdminDAO:
    def buscar_por_usuario(self, usuario):
        return session_dao.query(AdminDB).filter_by(usuario=usuario).first()

    def validar_login(self, usuario, senha):
        admin = self.buscar_por_usuario(usuario)
        if admin and check_password_hash(admin.senha_hash, senha):
            return True
        return False

aluno_dao = AlunoDAO(session_dao)
avaliador_dao = AvaliadorDAO(session_dao)
acao_dao = AcaoDAO(session_dao)
acao_realizadasDAO = AcaoRealizadaDAO(session_dao)
recompensa_dao = RecompensaDAO(session_dao)
resgate_dao = ResgateDAO(session_dao, recompensa_dao=recompensa_dao)
admin_dao = AdminDAO()
