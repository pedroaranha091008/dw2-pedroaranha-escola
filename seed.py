from app.database import init_db, get_session
from app.models import Aluno, Turma
from datetime import date
import random

NAMES = [
    "Ana Silva","Bruno Costa","Carla Souza","Daniel Lima","Eduarda Alves",
    "Felipe Ramos","Gabriela Nunes","Henrique Pinto","Isabela Rocha","João Paulo",
    "Karla Dias","Lucas Vieira","Mariana Freitas","Nico Santos","Olivia Moreira",
    "Pedro Aranha","Quenia Moraes","Rafael Teixeira","Sofia Pereira","Thiago Gomes"
]

def seed():
    init_db()
    with get_session() as s:
        # criar turmas
        turmas = [
            Turma(nome="1A", capacidade=5),
            Turma(nome="2B", capacidade=6),
            Turma(nome="3C", capacidade=8)
        ]
        for t in turmas:
            s.add(t)
        s.commit()
        for i, name in enumerate(NAMES):
            ano = random.randint(2006, 2016)
            mes = random.randint(1,12)
            dia = random.randint(1,28)
            nascimento = date(ano, mes, dia)
            aluno = Aluno(nome=name, data_nascimento=nascimento, email=f"{name.split()[0].lower()}@exemplo.com")
            # alguns alunos já ativos em turmas até capacidade
            if i < 10:
                aluno.status = "ativo"
                aluno.turma_id = turmas[i % len(turmas)].id
            s.add(aluno)
        s.commit()

if __name__ == "__main__":
    seed()
    print("Seed completo.")
