import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'

def test_crud_flow():
    # criar turma
    r = client.post('/turmas', json={'nome':'T1','capacidade':5})
    assert r.status_code == 200
    turma = r.json()
    # criar aluno
    r = client.post('/alunos', json={'nome':'Teste','data_nascimento':'2010-01-01','email':'t@ex.com'})
    assert r.status_code == 200
    aluno = r.json()
    # matricular
    r = client.post('/matriculas', json={'aluno_id': aluno['id'], 'turma_id': turma['id']})
    assert r.status_code == 200
    # listar alunos na turma
    r = client.get(f"/alunos?turma_id={turma['id']}&status=ativo")
    assert r.status_code == 200
    found = r.json()
    assert any(a['id'] == aluno['id'] for a in found)
