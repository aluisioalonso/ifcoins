from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import enum

Base = declarative_base()

class AlunoDB(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha_hash = Column(String)
    saldo = Column(Float, default=0)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    acoes_realizadas = relationship("AcaoRealizadaAlunoDB", back_populates="aluno")
    resgates = relationship("ResgateDB", back_populates="aluno")

    def __repr__(self):
        return f"<AlunoDB(email='{self.email}', nome='{self.nome}', saldo={self.saldo})>"





class AvaliadorDB(Base):
    __tablename__ = 'avaliadores'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha_hash = Column(String)
    status = Column(String, default='pendente')  # pendente / aprovado / rejeitado

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<AvaliadorDB(email='{self.email}', nome='{self.nome}', status={self.status})>"


class AcaoDB(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    valor = Column(Integer, default=0)

    acoes_realizadas = relationship("AcaoRealizadaAlunoDB", back_populates="acao")

    def __repr__(self):
        return (
            f"<AcaoDB(id={self.id}, nome='{self.nome}', valor={self.valor},descricao={self.descricao}')>"
        )

class AcaoRealizadaAlunoDB(Base):
    __tablename__ = 'acoes_realizadas'

    id = Column(Integer, primary_key=True)
    email_aluno = Column(String, ForeignKey('alunos.email'))
    id_acao = Column(Integer, ForeignKey('acoes.id'))
    comentarios_aluno = Column(String)
    link = Column(String, nullable=True)
    valor = Column(Integer, default=0)
    status = Column(String, default='pendente')  # pendente/aprovada/rejeitada
    data_envio = Column(DateTime, default=datetime.now())


    aluno = relationship("AlunoDB", back_populates="acoes_realizadas")
    acao = relationship("AcaoDB", back_populates="acoes_realizadas")

    def __repr__(self):
        return (
            f"<AcaoRealizadaAlunoDB(id={self.id}, aluno='{self.email_aluno}', "
            f"acao_id={self.id_acao}, status='{self.status}, valor='{self.valor}')>"
        )

class RecompensaDB(Base):
    __tablename__ = 'recompensas'

    id = Column(Integer, primary_key=True)
    tipo = Column(String)  # antes era nome
    descricao = Column(String)
    valor = Column(Float)   # antes era custo
    link = Column(String, nullable=True)
    vagas = Column(Integer, default=0)
    data_expiracao = Column(DateTime, nullable=True)
    resgates = relationship("ResgateDB", back_populates="recompensa")

    def __repr__(self):
        return (
            f"<RecompensaDB(id={self.id}, tipo='{self.tipo}', valor={self.valor}, vagas={self.vagas}, link={self.link}, data_expiracao={self.data_expiracao})>"
        )


class ResgateDB(Base):
    __tablename__ = 'resgates'

    id = Column(Integer, primary_key=True)
    aluno_email = Column(String, ForeignKey('alunos.email'))
    recompensa_id = Column(Integer, ForeignKey('recompensas.id'))
    valor_resgatado = Column(Integer)
    data_resgate = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pendente')  # pendente / entregue / cancelado

    aluno = relationship("AlunoDB", back_populates="resgates")
    recompensa = relationship("RecompensaDB", back_populates="resgates")

    def __repr__(self):
        return (
            f"<ResgateDB(id={self.id}, aluno='{self.aluno_email}', "
            f"recompensa_id={self.recompensa_id}, status='{self.status}')>"
        )

class AdminDB(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
