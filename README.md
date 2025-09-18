# Escola (DW2)

Projeto exemplo para gestão de turmas e alunos com FastAPI + SQLite.

Pré-requisitos
--------------
- Python 3.11+ instalado (adicionar ao PATH)
- Git (opcional)

Instalação e execução (Windows PowerShell)
----------------------------------------

```powershell
# clonar repositório (se ainda não clonou)
git clone https://github.com/pedroaranha091008/dw2-pedroaranha-escola.git
cd dw2-pedroaranha-escola

# criar e ativar virtualenv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# instalar dependências
pip install -r requirements.txt

# gerar seed (cria database)
python seed.py

# rodar servidor
uvicorn app.main:app --reload
```

Front-end
---------
- Arquivo `frontend/index.html` é um cliente simples que consome os endpoints do backend. Para testes locais, abra `frontend/index.html` no navegador enquanto o servidor FastAPI está rodando (ou sirva a pasta `frontend` com um servidor estático se preferir).

Endpoints principais
- GET /health
- GET /turmas
- POST /turmas
- GET /alunos?search=&turma_id=&status=&age_min=&age_max=&order=&limit=&offset=
- POST /alunos
- PUT /alunos/{id}
- DELETE /alunos/{id}
- POST /matriculas (body: aluno_id, turma_id)

Seeds
-----
- `python seed.py` cria 20 alunos de exemplo e 3 turmas.

Notas
-----
- O frontend realiza validações e exibe erros via toasts; a validação de faixa etária (>=5 anos) também é aplicada no backend.
- O projeto já possui tag `v1.0.0` criada e enviada ao GitHub.

Contribuições
-------------
- Pull requests são bem-vindos. Para rodar os testes (quando adicionados), siga as instruções que serão incluídas no README.

