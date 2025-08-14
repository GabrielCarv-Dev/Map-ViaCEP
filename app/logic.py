# app/logic.py

def normalize_cep(cep: str) -> str:
    """Remove tudo que não for dígito."""
    return "".join(c for c in cep if c.isdigit())


def is_valid_cep(cep: str) -> bool:
    """
    Valida um CEP brasileiro:
    - Normaliza para só dígitos
    - Verifica se tem exatamente 8 dígitos
    """
    cep_limpo = normalize_cep(cep)
    return len(cep_limpo) == 8


def build_geocode_queries(enderecojson: dict) -> list:
    """
    Monta, em ordem de prioridade, as consultas para geocodificação
    a partir de um dicionário no formato do ViaCEP.
    Retorna uma lista com strings (consultas textuais) e, por fim, um
    fallback por CEP como dict {"postalcode": "<cep>", "country": "Brazil"}.
    """
    logradouro = (enderecojson.get("logradouro") or "").strip()
    bairro     = (enderecojson.get("bairro") or "").strip()
    cidade     = (enderecojson.get("localidade") or "").strip()
    uf         = (enderecojson.get("uf") or "").strip()
    cep_norm   = (enderecojson.get("cep") or "").replace("-", "").strip()

    queries = []

    # A) Completo (logradouro, opcional bairro, cidade, UF)
    if logradouro and cidade and uf:
        rua_bairro = f"{logradouro}" + (f", {bairro}" if bairro else "")
        queries.append(f"{rua_bairro}, {cidade}, {uf}, Brazil")

    # B) Sem logradouro: bairro + cidade + UF
    if bairro and cidade and uf:
        queries.append(f"{bairro}, {cidade}, {uf}, Brazil")

    # C) Só cidade + UF
    if cidade and uf:
        queries.append(f"{cidade}, {uf}, Brazil")

    # D) Fallback por CEP (postal code)
    if cep_norm:
        queries.append({"postalcode": cep_norm, "country": "Brazil"})

    return queries
