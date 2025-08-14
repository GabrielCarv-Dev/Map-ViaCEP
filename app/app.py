
import streamlit as st
import requests as rq

# --- Tirar barra lateral ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Bora te achar.')


# --- Principal caixa do form ---
cepapp = st.form('capapp') # Principal caixa do form

caixa_cep =  cepapp.text_input("coloque seu cep aqui:")
ceplimpo = ''.join(c for c in caixa_cep if c.isdigit()) # Confirma apenas os números tirando simbolos caso o usuário forneça

submit = cepapp.form_submit_button("procurar")

# --- Condição para o cep ---
if submit:
    if len(ceplimpo) != 8:
        invalido = st.markdown(
            "<span style='color:red'>CEP tem 8 numeros</span>",
            unsafe_allow_html=True
        )
    elif ceplimpo.isdigit() == False:
        invalido = st.markdown(
            "<span style='color:red'>Número inválido</span>",
            unsafe_allow_html=True
        )
    else:
        st.session_state["cep"] = ceplimpo
        st.switch_page("pages/pagina2.py")






