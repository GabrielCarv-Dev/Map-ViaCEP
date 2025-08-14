# Consulta CEP + Mapa (Python + Streamlit)

Pequeno webapp em Python/Streamlit que recebe um CEP do usuário, consulta a API do ViaCEP e mostra a localização aproximada em um mapa interativo.

Projeto criado para:
- Aprender consumo de API em Python
- Treinar uso de bibliotecas como `requests`, `geopy` e `folium`
- Iniciar práticas de DevOps em um app real

## Tecnologias e bibliotecas usadas
- Frontend/backend: [Streamlit](https://streamlit.io/)
- API de CEP: [ViaCEP](https://viacep.com.br)
- Geocodificação: geopy (Nominatim)
- Mapas: folium + streamlit-folium
- Outros: requests

## Práticas DevOps já implementadas
- Dockerfile otimizado (Python slim, cache de dependências)
- .dockerignore para reduzir tamanho de build
- Pipeline CI/CD no GitHub Actions:
  - Executa testes automatizados (`pytest`)
  - Faz build da imagem Docker
- Testes unitários:
  - Validação de CEP
  - Montagem de query de geocodificação

## Como rodar localmente
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar o app
streamlit run app/app.py
```

## Rodando com Docker
```bash
# Build
docker build -t consulta-cep .

# Run
docker run --rm -p 8501:8501 consulta-cep
```
Acesse em: http://localhost:8501

## Estrutura do repositório
```
app/
  app.py
  pages/
    pagina2.py
tests/
  test_app.py
.github/workflows/
  ci.yml
Dockerfile
requirements.txt
README.md
LICENSE
```
