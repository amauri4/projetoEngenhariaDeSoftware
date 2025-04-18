import json
import pytest
from unittest.mock import MagicMock, mock_open
from models.CategoriasHabito import CategoriaHabito
from utils.sync import sync_categorias_from_json

@pytest.fixture
def mock_db():
    mock_db = MagicMock()

    categorias_existentes = {
        "Saúde": CategoriaHabito(nome="Saúde"),
        "Alimentação": CategoriaHabito(nome="Alimentação"),
    }

    def fake_filter_by(**kwargs):
        nome = kwargs.get("nome")
        mock_query = MagicMock()
        mock_query.first.return_value = categorias_existentes.get(nome)
        return mock_query

    mock_query = MagicMock()
    mock_query.filter_by.side_effect = fake_filter_by
    mock_db.query.return_value = mock_query

    return mock_db

@pytest.fixture
def mock_file_system(monkeypatch):
    fake_json = json.dumps({
        "categorias": ["Saúde", "Alimentação"],
        "habitos": [
            {"nome": "Beber Água", "descricao": "Beber 2L de água por dia", "categoria": "Saúde"},
            {"nome": "Comer Frutas", "descricao": "Comer 3 porções de frutas por dia", "categoria": "Alimentação"}
        ]
    })

    monkeypatch.setattr("builtins.open", mock_open(read_data=fake_json))

def test_sync_categorias_from_json(mock_db, mock_file_system):
    sync_categorias_from_json(mock_db)

    assert mock_db.add.call_count == 2

    habitos_adicionados = [call[0][0].nome for call in mock_db.add.call_args_list]

    assert "Beber Água" in habitos_adicionados
    assert "Comer Frutas" in habitos_adicionados
