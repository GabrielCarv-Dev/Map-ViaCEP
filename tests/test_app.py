# tests/test_app.py

from app.logic import normalize_cep, is_valid_cep, build_geocode_queries


def test_normalize_cep():
    assert normalize_cep("72015-035") == "72015035"
    assert normalize_cep(" 72 015 035 ") == "72015035"
    assert normalize_cep("abcdef") == ""


def test_is_valid_cep():
    # válidos
    assert is_valid_cep("12345678") is True
    assert is_valid_cep("12345-678") is True
    assert is_valid_cep(" 12 345 678 ") is True
    assert is_valid_cep("00000000") is True

    # inválidos
    assert is_valid_cep("1234567") is False     # 7 dígitos
    assert is_valid_cep("123456789") is False   # 9 dígitos
    assert is_valid_cep("abcdefgh") is False    # sem dígitos


def test_build_geocode_queries_completo():
    endereco = {
        "logradouro": "Quadra CSA 3",
        "bairro": "Taguatinga Sul",
        "localidade": "Brasília",
        "uf": "DF",
        "cep": "72015035",
    }
    queries = build_geocode_queries(endereco)
    assert queries[0] == "Quadra CSA 3, Taguatinga Sul, Brasília, DF, Brazil"
    assert queries[1] == "Taguatinga Sul, Brasília, DF, Brazil"
    assert queries[2] == "Brasília, DF, Brazil"
    assert queries[-1] == {"postalcode": "72015035", "country": "Brazil"}


def test_build_geocode_queries_sem_logradouro():
    endereco = {
        "logradouro": "",
        "bairro": "Taguatinga Sul",
        "localidade": "Brasília",
        "uf": "DF",
        "cep": "72015035",
    }
    queries = build_geocode_queries(endereco)
    assert queries[0] == "Taguatinga Sul, Brasília, DF, Brazil"
    assert queries[1] == "Brasília, DF, Brazil"
    assert queries[-1] == {"postalcode": "72015035", "country": "Brazil"}


def test_build_geocode_queries_so_cidade_uf():
    endereco = {
        "logradouro": "",
        "bairro": "",
        "localidade": "Brasília",
        "uf": "DF",
        "cep": "72015035",
    }
    queries = build_geocode_queries(endereco)
    assert queries[0] == "Brasília, DF, Brazil"
    assert queries[-1] == {"postalcode": "72015035", "country": "Brazil"}


def test_build_geocode_queries_somente_cep():
    endereco = {
        "logradouro": "",
        "bairro": "",
        "localidade": "",
        "uf": "",
        "cep": "72015035",
    }
    queries = build_geocode_queries(endereco)
    # só o fallback por CEP
    assert queries == [{"postalcode": "72015035", "country": "Brazil"}]
