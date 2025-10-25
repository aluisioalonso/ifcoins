from werkzeug.security import generate_password_hash
from database.database import session_dao
from models.modelosDB import AdminDB

def criar_admin_padrao():
    usuario = 'admin'
    senha = '1234'

    admin_existente = session_dao.query(AdminDB).filter_by(usuario=usuario).first()
    if admin_existente:
        print(f"⚠️ Admin '{usuario}' já existe.")
        return

    novo_admin = AdminDB(
        usuario=usuario,
        senha_hash=generate_password_hash(senha)
    )

    session_dao.add(novo_admin)
    session_dao.commit()
    print(f"✅ Admin '{usuario}' criado com sucesso! (senha: {senha})")

if __name__ == '__main__':
    criar_admin_padrao()
