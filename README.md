# Escola (DW2)

Projeto exemplo para gestão de turmas e alunos com FastAPI + SQLite.

Como rodar (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; uvicorn app.main:app --reload
```

Endpoints principais:
- GET /health
- GET /turmas
- POST /turmas
- GET /alunos?search=&turma_id=&status=
- POST /alunos
- PUT /alunos/{id}
- DELETE /alunos/{id}
- POST /matriculas (body: aluno_id, turma_id)

Seeds:
- `python seed.py` cria dados de exemplo
