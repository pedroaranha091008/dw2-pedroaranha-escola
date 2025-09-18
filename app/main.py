from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from sqlmodel import select, text
from datetime import date, datetime, timedelta

from .database import init_db, get_session
from .models import Aluno, Turma

app = FastAPI(title="Escola API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/turmas", response_model=List[Turma])
def get_turmas():
    with get_session() as s:
        return s.exec(select(Turma)).all()

@app.post("/turmas", response_model=Turma)
def create_turma(turma: Turma):
    if turma.capacidade <= 0:
        raise HTTPException(status_code=400, detail="Capacidade deve ser maior que zero")
    with get_session() as s:
        s.add(turma)
        s.commit()
        s.refresh(turma)
        return turma

@app.get("/alunos", response_model=List[Aluno])
def get_alunos(
    search: Optional[str] = None,
    turma_id: Optional[int] = None,
    status: Optional[str] = None,
    age_min: Optional[int] = Query(None, alias="age_min"),
    age_max: Optional[int] = Query(None, alias="age_max"),
    order: Optional[str] = Query(None),
    limit: Optional[int] = Query(0),
    offset: Optional[int] = Query(0),
):
    with get_session() as s:
        q = select(Aluno)
        if search:
            q = q.where(Aluno.nome.contains(search))
        if turma_id:
            q = q.where(Aluno.turma_id == turma_id)
        if status:
            q = q.where(Aluno.status == status)
        # filtro por idade (calcular usando data_nascimento)
        today = date.today()
        if age_min is not None:
            # data de nascimento máxima permitida
            max_dob = date(today.year - age_min, today.month, today.day)
            q = q.where(Aluno.data_nascimento <= max_dob)
        if age_max is not None:
            # data de nascimento mínima permitida para idade máxima (nascidos a partir desta data têm idade <= age_max)
            min_dob = date(today.year - age_max, today.month, today.day)
            q = q.where(Aluno.data_nascimento >= min_dob)
        # ordenação segura
        if order in ("nome", "data_nascimento", "status"):
            q = q.order_by(text(order))
        results = s.exec(q)
        if limit and limit > 0:
            results = results.limit(limit).offset(offset)
        return results.all()

@app.post("/alunos", response_model=Aluno)
def create_aluno(aluno: Aluno):
    # Validação de faixa etária (exemplo: mínimo 5 anos)
    age = _calculate_age(aluno.data_nascimento)
    if age < 5:
        raise HTTPException(status_code=400, detail="Aluno deve ter pelo menos 5 anos")
    with get_session() as s:
        s.add(aluno)
        s.commit()
        s.refresh(aluno)
        return aluno

@app.put("/alunos/{aluno_id}", response_model=Aluno)
def update_aluno(aluno_id: int, aluno: Aluno):
    with get_session() as s:
        db = s.get(Aluno, aluno_id)
        if not db:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        db.nome = aluno.nome
        db.data_nascimento = aluno.data_nascimento
        db.email = aluno.email
        db.status = aluno.status
        db.turma_id = aluno.turma_id
        s.add(db)
        s.commit()
        s.refresh(db)
        return db

@app.delete("/alunos/{aluno_id}")
def delete_aluno(aluno_id: int):
    with get_session() as s:
        db = s.get(Aluno, aluno_id)
        if not db:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        s.delete(db)
        s.commit()
        return {"detail": "Aluno removido"}

@app.post("/matriculas")
def matricula(payload: dict):
    aluno_id = payload.get("aluno_id")
    turma_id = payload.get("turma_id")
    if not aluno_id or not turma_id:
        raise HTTPException(status_code=400, detail="aluno_id e turma_id são obrigatórios")
    with get_session() as s:
        turma = s.get(Turma, turma_id)
        if not turma:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        # contar alunos ativos na turma
        q = select(Aluno).where(Aluno.turma_id == turma_id, Aluno.status == "ativo")
        ocupacao = s.exec(q).count()
        if ocupacao >= turma.capacidade:
            raise HTTPException(status_code=400, detail="Turma cheia")
        aluno = s.get(Aluno, aluno_id)
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        aluno.status = "ativo"
        aluno.turma_id = turma_id
        s.add(aluno)
        s.commit()
        s.refresh(aluno)
        return {"detail": "Matrícula realizada", "aluno": aluno}

def _calculate_age(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
