import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from plots.plots import *
from layout.layout import *

im = Image.open("image/ufsc.jpg")
im2 = Image.open("image/brasao.png")
st.set_page_config(page_title="UFSC em Dados", page_icon=im, layout="wide")

st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)


st.markdown("<h1 style='font-size:250%; text-align: center; color: #05A854; padding: 0px 0px;'" +
                ">UFSC em Dados</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 10px 0px;'" +
            ">Última atualização: 01/04/2023</h3>", unsafe_allow_html=True)

st.markdown("""<style> .css-hxt7ib.e1fqkh3o5 {margin-top: -90px;}</style>""", unsafe_allow_html=True)

with st.sidebar:
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write('')
    with col2:
        st.image(im2, caption='Universidade Federal de Santa Catarina')
    with col3:
        st.write('')

    st.markdown('---')
    basedados = st.selectbox("Selecione os dados para sua análise:",
                             options=["População de Estudantes",
                                      "População de Funcionários",
                                      "Vagas no Vestibular"], index=0)

    if basedados == "População de Estudantes":
        df = load_google_sheet(tabela="1")
        df = tratamento1(df)
    elif basedados == "População de Funcionários":
        df = load_google_sheet(tabela="2")
        df = tratamento1(df)
    elif basedados == "Vagas no Vestibular":
        df = load_google_sheet(tabela="3")
        df = tratamento2(df)

        agrupamento = st.radio('Selecione o agrupamento:', ['Cursos', 'Centros', 'Campus'], index=0, key=9, horizontal=True)

        if agrupamento == 'Cursos':
            df = df.groupby("CURSO").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        elif agrupamento == 'Centros':
            df = df.groupby("CENTRO DE ENSINO").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        elif agrupamento == 'Campus':
            df = df.groupby("CAMPUS").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        df = df.astype(int)

    with st.expander("🎲️ Filtrar os dados"):
        ano_max = int(df['ANO'].max())
        ano_min = int(df['ANO'].min())
        ano_range_min, ano_range_max = st.slider('Selecione o intervalo de ANOS:',
                                                  min_value=ano_min, max_value=ano_max, value=(ano_min, ano_max))

        mask_valor = (df['ANO'] >= int(ano_range_min)) & (df['ANO'] <= int(ano_range_max))

        colunas = df.columns.unique().tolist()
        selected_colunas = st.multiselect("Selecione as colunas da Tabela:",
                                          options=colunas, default=colunas)
        st.markdown('---')
        df = df.loc[:, selected_colunas]
        df = df.loc[mask_valor]


st.markdown('---')

if basedados == "População de Estudantes" or basedados == "População de Funcionários":
    st.markdown("<h2 style='font-size:150%; text-align: center; color: #05A854; padding: 0px 0px 15px 0px;'" +
                ">"+basedados+" entre "+str(ano_range_min)+" a "+str(ano_range_max)+" - Tabela Dinâmica</h2>", unsafe_allow_html=True)

selected_rows = agg_tabela(df, True)

st.text('')
tab1, tab2, tab3, tab4 = st.tabs(["LABORATÓRIO 🔬", "ANÁLISE EXPLORATÓRIA 🔎", "DASHBOARD 📊" , 'CONHEÇA MAIS O APP ❓'])

with tab1:
    if len(selected_rows) == 0:
        if basedados == "População de Estudantes":
            estudantes(df, selected_rows, basedados)
        elif basedados == "População de Funcionários":
            estudantes(df, selected_rows, basedados)
        elif basedados == "Vagas no Vestibular":
            vagasvestibular(df, selected_rows, basedados)
        st.text('')
    elif len(selected_rows) != 0:
        if basedados == "População de Estudantes":
            estudantes(selected_rows, selected_rows, basedados)
        elif basedados == "População de Funcionários":
            estudantes(selected_rows, selected_rows, basedados)
        elif basedados == "Vagas no Vestibular":
            estudantes(selected_rows, selected_rows, basedados)
with tab2:
    if len(selected_rows) == 0:
        relatorio(df)
    elif len(selected_rows) != 0:
        relatorio(selected_rows)
with tab3:
    st.text('Ainda Nada...')
with tab4:
    boasvindas()




rodape()