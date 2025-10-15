from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AlunoDB(Base):
    __tablename__ = 'alunos'

    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)
    saldo = Column(Integer, default=0)

    acoes_realizadas = relationship("AcaoRealizadaAlunoDB", back_populates="aluno")
    resgates = relationship("ResgateDB", back_populates="aluno")

    def __repr__(self):
        return f"<AlunoDB(email='{self.email}', nome='{self.nome}', saldo={self.saldo})>"

class AvaliadorDB(Base):
    __tablename__ = 'avaliadores'

    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)
    aprovado = Column(Boolean, default=False)

    def __repr__(self):
        return f"<AvaliadorDB(email='{self.email}', nome='{self.nome}', aprovado={self.aprovado})>"

class AcaoDB(Base):
    __tablename__ = 'acoes'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    valor = Column(Integer, default=0)
    status = Column(String, default='pendente')

    acoes_realizadas = relationship("AcaoRealizadaAlunoDB", back_populates="acao")

    def __repr__(self):
        return (
            f"<AcaoDB(id={self.id}, nome='{self.nome}', valor={self.valor}, status='{self.status}')>"
        )

class AcaoRealizadaAlunoDB(Base):
    __tablename__ = 'acoes_realizadas'

    id = Column(Integer, primary_key=True)
    email_aluno = Column(String, ForeignKey('alunos.email'))
    id_acao = Column(Integer, ForeignKey('acoes.id'))
    comentarios_aluno = Column(String)
    valor = Column(Integer, default=0)
    status = Column(String, default='pendente')  # pendente/aprovada/rejeitada
    data_envio = Column(DateTime, default=datetime.utcnow)

    aluno = relationship("AlunoDB", back_populates="acoes_realizadas")
    acao = relationship("AcaoDB", back_populates="acoes_realizadas")

    def __repr__(self):
        return (
            f"<AcaoRealizadaAlunoDB(id={self.id}, aluno='{self.email_aluno}', "
            f"acao_id={self.id_acao}, status='{self.status}')>"
        )

class RecompensaDB(Base):
    __tablename__ = 'recompensas'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    custo = Column(Integer)
    estoque = Column(Integer, default=0)

    resgates = relationship("ResgateDB", back_populates="recompensa")

    def __repr__(self):
        return (
            f"<RecompensaDB(id={self.id}, nome='{self.nome}', custo={self.custo}, estoque={self.estoque})>"
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
