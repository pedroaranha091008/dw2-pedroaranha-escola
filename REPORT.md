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
Durante o desenvolvimento utilizei prompts para gerar trechos repetitivos e acelerar a implementação; abaixo 6 prompts reais (ajustados para o contexto) com o trecho aceito/editado e por quê:

1) Gerar models SQLModel para Turma e Aluno
	- Prompt: "Gerar models SQLModel para entidades Turma(id,nome,capacidade) e Aluno(id,nome,data_nascimento,email?,status,turma_id?) com relacionamentos"
	- Trecho aceito/editado: classe `Turma` e `Aluno` em `app/models.py` (ajustei tipos e nomes de campos, e adicionei Relationship para facilitar consultas).
	- Por quê: acelerou criação de models e evitou erros de mapeamento; adaptei validações e defaults manualmente.

2) Criar endpoint básico FastAPI /alunos
	- Prompt: "Escrever endpoint FastAPI GET/POST/PUT/DELETE para model Aluno usando SQLModel e sessão".
	- Trecho aceito/editado: handlers em `app/main.py` (mantive a estrutura sugerida e acrescentei validações de idade e mensagens de erro claras).
	- Por quê: forneceu esqueleto rápido; editei respostas e tratamento de HTTP codes.

3) Script seed plausível
	- Prompt: "Gerar um script seed que crie 20 nomes plausíveis e 3 turmas com capacidades diferentes usando SQLModel Session".
	- Trecho aceito/editado: `seed.py` com lista de 20 nomes e lógica de distribuição entre turmas; ajustei anos de nascimento para manter faixas coerentes.
	- Por quê: economizou tempo de criação de dados e permitiu foco nas validações.

4) Validação de faixa etária (backend)
	- Prompt: "Adicionar validação no endpoint POST /alunos para assegurar que aluno tenha pelo menos 5 anos, retornar HTTP 400 com mensagem clara".
	- Trecho aceito/editado: ver `create_aluno` em `app/main.py` (insira a verificação de idade e raise HTTPException com detail amigável).
	- Por quê: garante regras de negócio no servidor; mantive a mesma mensagem no cliente para consistência UX.

5) Toasts acessíveis e animação
	- Prompt: "Exemplo simples de toasts acessíveis em JS (role=alert, aria-live) com botão fechar e animação CSS".
	- Trecho aceito/editado: implementação em `frontend/index.html` e estilos em `frontend/css/style.css` (adaptei classes e tempos de animação).
	- Por quê: trouxe padrão acessível e rapidamente integrável, editei para combinar com o estilo do projeto.

6) Filtros avançados + paginação
	- Prompt: "Implementar filtros combináveis (search, turma_id, status, age_min, age_max) e opções de ordenação; retornar resultados paginados (limit/offset)".
	- Trecho aceito/editado: backend `/alunos` em `app/main.py` (parâmetros age_min/age_max/order/limit/offset) e frontend query-building em `frontend/index.html`.
	- Por quê: reduziu esforço ao lidar com query params e ordenação; refinei cálculo de datas para filtros por idade.

Esses prompts aceleraram tarefas repetitivas; em todos os casos revisei e ajustei os trechos gerados para garantir segurança, mensagens de erro claras e integração com o restante do código.

Limitações e melhorias futuras
----------------------------
- Interface mínima e sem build tool.
- Testes automatizados faltantes (sugerido: pytest + httpx)
- Adicionar paginação no backend (já tem support limit/offset, mas front usa paginação cliente por padrão).
- Melhorar UX dos formulários e adicionar edição inline.

