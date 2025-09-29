from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AlunoDB(Base):
    __tablename__ = 'alunos'
    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)
    saldo = Column(Integer, default=0)
    acoes = relationship("AcaoDB", back_populates="aluno")

class MestreDB(Base):
    __tablename__ = 'mestres'
    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)
    aprovado = Column(Boolean, default=False)

class AcaoDB(Base):
    __tablename__ = 'acoes'
    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    aluno_email = Column(String, ForeignKey('alunos.email'))
    valor = Column(Integer, default=0)
    status = Column(String, default='pendente')
    aluno = relationship("AlunoDB", back_populates="acoes")
