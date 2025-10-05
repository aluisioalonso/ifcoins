from database.database import *

alunoDao = AlunoDAO()

lista = alunoDao.buscar_por_email()
print(lista)