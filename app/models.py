from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Turma(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    capacidade: int
    alunos: List["Aluno"] = Relationship(back_populates="turma")

class Aluno(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    data_nascimento: date
    email: Optional[str] = None
    status: str = "inativo"  # 'ativo' ou 'inativo'
    turma_id: Optional[int] = Field(default=None, foreign_key="turma.id")
    turma: Optional[Turma] = Relationship(back_populates="alunos")
