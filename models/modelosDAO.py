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

    acoes = relationship("AcaoDB", back_populates="aluno")
    resgates = relationship("ResgateDB", back_populates="aluno")

    def __repr__(self):
        senha_oculta = '***' if self.senha else 'N/A'
        return (
            f"<AlunoDB(email='{self.email}', nome='{self.nome}', "
            f"saldo='{self.saldo}', senha='{senha_oculta}')>"
        )


class AvaliadorDB(Base):
    __tablename__ = 'avaliadores'
    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)
    aprovado = Column(Boolean, default=False)

    def __repr__(self):
        senha_oculta = '***' if self.senha else 'N/A'
        return (
            f"<AvaliadorDB(email='{self.email}', nome='{self.nome}', "
            f"aprovado='{self.aprovado}', senha='{senha_oculta}')>"
        )


class AcaoRealizadaAlunoDB(Base):
    __tablename__ = 'acaorealizada'
    id = Column(Integer, primary_key=True)
    email_aluno = Column(String)
    id_acao = Column(String)
    comentarios_aluno = Column(String)
    valor = Column(Integer, default=0)
    status = Column(Boolean, default=False)


    def __repr__(self):
        return f"<AcaoDB(id={self.id})>"

class AcaoDB(Base):
    __tablename__ = 'acoes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    valor = Column(Integer, default=0)

    def __repr__(self):
        return f"<AcaoDB(id={self.id}, status='{self.status}')>"


class RecompensaDB(Base):
    __tablename__ = 'recompensas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    custo = Column(Integer)  # Custo em IFCoins
    estoque = Column(Integer, default=0)

    # povo, eu deixei um para muitos: uma recompensa pode estar em muitos resgates, ok???
    resgates = relationship("ResgateDB", back_populates="recompensa")

    def __repr__(self):
        return f"<RecompensaDB(id={self.id}, nome='{self.nome}', custo='{self.custo}', estoque='{self.estoque}')>"


class ResgateDB(Base):
    __tablename__ = 'resgates'
    id = Column(Integer, primary_key=True)

    aluno_email = Column(String, ForeignKey('alunos.email'))
    recompensa_id = Column(Integer, ForeignKey('recompensas.id'))

    valor_resgatado = Column(Integer)
    data_resgate = Column(DateTime, default=datetime.utcnow)
    # status: 'pendente', 'entregue', 'cancelado'
    status = Column(String, default='pendente')

    aluno = relationship("AlunoDB", back_populates="resgates")
    recompensa = relationship("RecompensaDB", back_populates="resgates")

    def __repr__(self):
        return f"<ResgateDB(id={self.id}, aluno='{self.aluno_email}', recompensa_id={self.recompensa_id}, status='{self.status}')>"