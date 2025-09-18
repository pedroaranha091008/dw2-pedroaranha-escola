REPORT - Projeto Escola

Resumo
-------
Projeto de gestão escolar com entidades Turma e Aluno. Backend em FastAPI + SQLModel + SQLite; frontend simples em HTML/CSS/vanilla JS com funcionalidades principais: CRUD de alunos e turmas, matrícula com validação de capacidade, filtros avançados, paginação cliente, export CSV/JSON, tema claro/escuro e acessibilidade básica.

Arquitetura
----------
- Cliente (frontend) faz requisições HTTP → Backend (FastAPI)
- FastAPI usa SQLModel (SQLAlchemy wrapper) para ORM → grava/consulta em SQLite (`app/database.db`)
- Fluxo: Request -> FastAPI Router -> Serviço/DB Session -> ORM -> SQLite -> resposta JSON

Tecnologias e versões
---------------------
- Python 3.11+ (recomendado)
- FastAPI 0.95.2
- SQLModel 0.0.8
- Uvicorn (para rodar o servidor)
- Frontend: HTML/CSS/Vanilla JS
- Ferramentas: Git, VSCode

Peculiaridades implementadas
---------------------------
Implementei as 3 obrigatórias e mais funcionalidades extras:

1) Validações custom (Back & Front)
	- Backend: validação de faixa etária mínima (>=5 anos) no endpoint `POST /alunos`.
	- Frontend: validação idêntica antes de enviar o formulário, com mensagens de erro exibidas via toasts.

2) Seed script com dados plausíveis
	- `seed.py` gera 20 alunos e 3 turmas com capacidades distintas; alguns alunos já estão ativos e atribuídos a turmas.

3) Testes de API (coleção HTTP)
	- `api.http` contém exemplos para health, turmas, alunos, matrículas, filtros, paginação e ordenação.

Funcionalidades adicionais implementadas
 - Filtros avançados no frontend (nome, turma, status, idade mínima/máxima) sem recarregar a página.
 - Ordenação persistida usando `localStorage` (nome, idade, status).
 - Paginação cliente + controles e export CSV/JSON da página atual.
 - Tema claro/escuro com persistência em `localStorage`.
 - Acessibilidade: skip-link, ARIA roles nos toasts, foco visível e navegação por teclado melhorada.
 - Toasters visuais com animação e dismiss.

Validações (exemplos)
---------------------
- Backend `POST /alunos` retorna 400 com mensagem clara se o aluno tiver menos de 5 anos.
- Backend `POST /turmas` exige `capacidade > 0`.
- Backend `POST /matriculas` valida capacidade da turma e retorna 400 se a turma estiver cheia.

Acessibilidade
--------------
- Skip link para pular ao conteúdo.
- Inputs e botões com foco visível (outline CSS) e ordem lógica de tabulação.
- Toasters usam `role="status"`/`aria-live="polite"` e recebem foco quando aparecem.

Como rodar (Windows PowerShell)
-------------------------------
1) Criar e ativar virtualenv

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2) Instalar dependências

```powershell
pip install -r requirements.txt
```

3) Gerar seed (cria `app/database.db`)

```powershell
python seed.py
```

4) Rodar servidor

```powershell
uvicorn app.main:app --reload
```

5) Abrir frontend

- Frontend está em `frontend/index.html`. Se rodar o servidor em outra porta, atualize os endpoints fetch no JS ou sirva o arquivo estático via um servidor simples.

Prompts do Copilot (exemplos)
----------------------------
Inclua aqui 6 prompts usados durante desenvolvimento, com trechos aceitos/editados e justificativa (ex.: geração de models, seed script, validações, toasts, filtros). Preencher na versão final.

Limitações e melhorias futuras
----------------------------
- Interface mínima e sem build tool.
- Testes automatizados faltantes (sugerido: pytest + httpx)
- Adicionar paginação no backend (já tem support limit/offset, mas front usa paginação cliente por padrão).
- Melhorar UX dos formulários e adicionar edição inline.

