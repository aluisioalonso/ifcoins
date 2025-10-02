from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.pessoas import Base, AlunoDB, MestreDB, AcaoDB

engine = create_engine('sqlite:///ifcoins.db')
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    print('estamos criando a estrututa do banco de dados')
    Base.metadata.create_all(engine)