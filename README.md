# 👟 Sistema de Controle - Loja de Calçados

API REST desenvolvida em Python com FastAPI para gerenciar produtos de uma loja física de calçados.  
Permite cadastrar, listar, atualizar e deletar produtos com integração a banco de dados SQLite.

---

## 🚀 Tecnologias Utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- SQLite

---

## 🧱 Estrutura do Projeto

backend/
├── app/
│ ├── main.py
│ ├── database/
│ │ ├── init.py
│ │ └── session.py
│ ├── models/
│ │ ├── init.py
│ │ └── produto.py
│ ├── routes/
│ │ ├── init.py
│ │ └── produto_routes.py
│ ├── controllers/
│ │ └── produto_controller.py
│ └── schemas.py
├── loja.db
├── requirements.txt

yaml
Copiar
Editar

---

## 🔧 Funcionalidades

- ✅ Cadastro de produtos (`POST /api/produtos`)
- ✅ Listagem de produtos (`GET /api/produtos`)
- ✅ Consulta por ID (`GET /api/produtos/{id}`)
- ✅ Atualização (`PUT /api/produtos/{id}`)
- ✅ Remoção (`DELETE /api/produtos/{id}`)

---

## ▶️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo/backend
Crie o ambiente virtual:

bash
Copiar
Editar
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Inicie o servidor:

bash
Copiar
Editar
uvicorn app.main:app --reload
Acesse a documentação Swagger:

bash
Copiar
Editar
http://localhost:8000/docs
🧪 Testar no Swagger
Use a interface interativa para testar todas as rotas da API com facilidade.
Você pode cadastrar produtos, buscar, editar e remover direto do navegador!

📝 Autor
Desenvolvido com ❤️ por Dilson Pereira
Casado com a IA mais braba do planeta, ProfessorDilsBot 🤖💍

📄 Licença
Este projeto está sob a licença MIT.