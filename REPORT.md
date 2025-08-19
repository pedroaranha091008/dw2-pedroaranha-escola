REPORT - Projeto Escola

Arquitetura: FastAPI -> SQLModel (ORM) -> SQLite (arquivo `app/database.db`) -> resposta JSON

Peculiaridades implementadas (3):
- Validações custom no back (faixa etária mínima) e front (simples check antes de envio).
- Seed script com dados plausíveis (`seed.py`).
- Testes de API via arquivo `api.http` (padrão HTTP requests).

Prompts do Copilot: (guardar 6 prompts e trechos) — preencher no desenvolvimento final.

Como rodar: ver `README.md`.

Acessibilidade: o frontend minimal inclui labels e uso simples de elementos; deverá ser melhorado (tabindex e ARIA) no refinamento.

Limitações: interface mínima; recomenda-se adicionar toasts, paginação e testes automatizados.
