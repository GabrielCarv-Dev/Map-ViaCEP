
import streamlit as st
import requests as rq
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from streamlit_folium import st_folium
import folium

# --- Tirar barra lateral ---
st.set_page_config(page_title="Página 2", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Sua Localização")

# --- Recupera CEP da sessão ---
cepinput = st.session_state.get("cep", "").strip()
if not cepinput:
    st.error("CEP não encontrado na sessão. Volte e preencha o formulário.")
    if st.button("Voltar"):
        st.switch_page("cep_lit.py")
    st.stop()

# --- Consulta CEP ---
try:
    resp = rq.get(f"https://viacep.com.br/ws/{cepinput}/json/", timeout=10)
    resp.raise_for_status()
    enderecojson = resp.json()
    if enderecojson.get("erro"):
        st.error("CEP não encontrado no ViaCEP.")
        st.stop()
except Exception as e:
    st.error(f"Falha ao consultar ViaCEP: {e}")
    st.stop()

logradouro = (enderecojson.get("logradouro") or "").strip()
bairro     = (enderecojson.get("bairro") or "").strip()
cidade     = (enderecojson.get("localidade") or "").strip()
uf         = (enderecojson.get("uf") or "").strip()
cep_norm   = (enderecojson.get("cep") or cepinput).replace("-", "").strip()

# --- geocodificação com fallback (Nominatim) ---
geolocator = Nominatim(user_agent="cep_lit_gabriel")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

queries = []
if logradouro:
    rua_bairro = f"{logradouro}" + (f", {bairro}" if bairro else "")
    queries.append(f"{rua_bairro}, {cidade}, {uf}, Brazil")
if bairro:
    queries.append(f"{bairro}, {cidade}, {uf}, Brazil")
if cidade and uf:
    queries.append(f"{cidade}, {uf}, Brazil")
queries.append({"postalcode": cep_norm, "country": "Brazil"})

location = None
for q in queries:
    try:
        location = geocode(q, timeout=10)
        if location:
            break
    except Exception:
        continue

if not location:
    st.warning("Não foi possível geocodificar este CEP.")
    st.write("Dados ViaCEP:", enderecojson)
    st.stop()

lat = float(location.latitude)
lon = float(location.longitude)
st.write("lat/lon:", lat, lon)


m = folium.Map(location=[lat, lon], zoom_start=14)
folium.Marker([lat, lon], tooltip="Local").add_to(m)
st_folium(m, height=420, width=700)

if st.button("Voltar"):
        st.switch_page("cep_lit.py")

# --- Dados do CEP ---
st.subheader("Endereço (ViaCEP)")
st.write({
    "CEP": cep_norm,
    "Logradouro": logradouro or "—",
    "Bairro": bairro or "—",
    "Cidade": cidade or "—",
    "UF": uf or "—"
})
