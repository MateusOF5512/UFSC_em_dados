import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from plots.plots import *
from layout.layout import *

im = Image.open("image/ufsc.jpg")
im2 = Image.open("image/brasao.png")
st.set_page_config(page_title="UFSC em Dados", page_icon=im, layout="wide")

st.markdown("""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """, unsafe_allow_html=True)


st.markdown("<h1 style='font-size:250%; text-align: center; color: #05A854; padding: 0px 0px;'" +
                ">UFSC em Dados</h1>", unsafe_allow_html=True)
st.markdown('---')

st.markdown("""<style> .css-1544g2n.e1fqkh3o4 {margin-top: -60px;}</style>""", unsafe_allow_html=True)
st.markdown("""<style> .css-uf99v8.egzxvld5 {margin-top: -50px;}</style>""", unsafe_allow_html=True)

with st.sidebar:
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write('')
    with col2:
        st.image(im2, caption='Universidade Federal de Santa Catarina')
    with col3:
        st.write('')

    st.markdown('---')
    st.text('')
    st.text('')

    st.markdown(
        "<h3 style='font-size:140%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px; margin-top: -40px;'" +
        ">Painel de controle:</h3>", unsafe_allow_html=True)

    basedados = st.selectbox("Selecione a tabela para análise:",
                             options=["População Universitária",
                                      "Vagas no Vestibular",
                                      "Inscritos no Vestibular"], index=0)

    if basedados == "População Universitária":
        agrupamento = st.radio('Selecione o agrupamento dos dados da tabela:',
                               ['Estudantes', 'Funcionários'], index=0, key=9,
                               horizontal=True)
        if agrupamento == 'Estudantes':
            df = load_google_sheet(tabela="1")
            df = tratamento1(df)

        elif agrupamento == 'Funcionários':
            df = load_google_sheet(tabela="2")
            df = tratamento1(df)

    elif basedados == "Vagas no Vestibular":
        df = load_google_sheet(tabela="3")
        df = tratamento2(df)

        agrupamento = st.radio('Selecione o agrupamento dos dados da Tabela:',
                               ['Curso', 'Centro de Ensino', 'Campus'], index=0, key=9, horizontal=True)

        if agrupamento == 'Curso':
            df = df.groupby("CURSO").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        elif agrupamento == 'Centro de Ensino':
            df = df.groupby("CENTRO DE ENSINO").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        elif agrupamento == 'Campus':
            df = df.groupby("CAMPUS").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        df = df.astype(int)

    elif basedados == "Inscritos no Vestibular":
        df = load_google_sheet(tabela="4")
        df = tratamento2(df)

        agrupamento = st.radio('Selecione o agrupamento dos dados da Tabela:',
                               ['Curso', 'Centro de Ensino', 'Campus'], index=0, key=91, horizontal=True)

        if agrupamento == 'Curso':
            df = df.groupby("CURSO").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        elif agrupamento == 'Centro de Ensino':
            df = df.groupby("CENTRO DE ENSINO").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)


        elif agrupamento == 'Campus':
            df = df.groupby("CAMPUS").sum().T.reset_index(drop=False).rename({'index': 'ANO'}, axis=1)

        df = df.astype(int)

    st.markdown('---')

    st.text('')
    st.text('')
    st.markdown(
        "<h3 style='font-size:120%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px; margin-top: -40px;'" +
        ">Manipulação dos dados e gráficos</h3>", unsafe_allow_html=True)

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

    grafico = st.selectbox('Tipo do Gráfico:',
                           ['Barra Simples', 'Linha Simples', 'Dispersão Simples', 'Barras Empilhadas', 'Barras Agrupadas',
                            'Multiplas Linhas', 'Multiplas Áreas', 'Área Normalizada'],
                           index=0, key=98)

    st.markdown("---")




if basedados == "População Universitária":
    st.markdown("<h3 style='font-size:140%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px; margin-top: -40px;'" +
                ">" + basedados + ": <b> n° de "  + agrupamento+" entre "+str(ano_range_min)+" - "+
                str(ano_range_max)+" | Tabela Dinâmica</b></h3>", unsafe_allow_html=True)
elif basedados == "Vagas no Vestibular" or basedados == "Inscritos no Vestibular":
    st.markdown("<h3 style='font-size:140%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px; margin-top: -50'" +
                ">" + basedados + ": <b> n° por " + agrupamento + " entre " + str(ano_range_min) + " - " +
                str(ano_range_max) + " | Tabela Dinâmica</b></h3>", unsafe_allow_html=True)


selected_rows = agg_tabela(df, True, key=83)

st.text('')
tab1, tab2, tab3, tab4 = st.tabs(["LABORATÓRIO 🔬", "DASHBOARD 📊" , "EXPLORAR DADOS 🔎", 'APP WEB ❓'])

with tab1:
    if len(selected_rows) == 0:
        if basedados == "População Universitária":
            populacao(df, selected_rows, grafico, basedados, agrupamento)
        elif basedados == "Vagas no Vestibular" or basedados == "Inscritos no Vestibular":
            vagasvestibular(df, selected_rows, grafico, basedados, agrupamento)
    elif len(selected_rows) != 0:
        if basedados == "População Universitária":
            populacao(selected_rows, selected_rows, grafico, basedados, agrupamento)
        elif basedados == "Vagas no Vestibular" or basedados == "Inscritos no Vestibular":
            vagasvestibular(df, selected_rows, grafico, basedados, agrupamento)
with tab2:
    st.text('Ainda Nada...')
with tab3:
    if len(selected_rows) == 0:
        relatorio(df, basedados, agrupamento)
    elif len(selected_rows) != 0:
        relatorio(selected_rows, basedados, agrupamento)
with tab4:
    boasvindas()




rodape()