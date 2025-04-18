import os
import json
import pytest
from app.models.CategoriasHabito import CategoriaHabito
from app.models.HabitoBase import HabitoBase
from app.utils.sync import sync_categorias_from_json  

@pytest.fixture
def sample_json(tmp_path):
    data = {
        "categorias": [
            {"id": 1, "nome": "Saúde"},
            {"id": 2, "nome": "Estudos"}
        ],
        "habitos": [
            {"nome": "Beber Água", "categoria_id": 1},
            {"nome": "Estudar 1h", "categoria_id": 2}
        ]
    }
    json_path = tmp_path / "categorias_habitos.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return json_path

def test_sync_from_valid_json(db_session, sample_json):
    sync_categorias_from_json(db_session, path=str(sample_json))

    categorias = db_session.query(CategoriaHabito).all()
    habitos = db_session.query(HabitoBase).all()

    assert len(categorias) == 2
    assert len(habitos) == 2

    saude = next((c for c in categorias if c.nome == "Saúde"), None)
    assert saude is not None

    habito = db_session.query(HabitoBase).filter_by(nome="Beber Água").first()
    assert habito is not None
    assert habito.categoria_id == saude.id
