import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from plots.plots import *
from layout.layout import *

im = Image.open("image/ufsc.jpg")
st.set_page_config(page_title="UFSC em Dados", page_icon=im, layout="wide")

st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

df = load_google_sheet()


col1, col2, col3 = st.columns([100, 1000, 100])
with col1:
    st.image(im)
with col2:
    st.text('')
    st.markdown("<h1 style='font-size:250%; text-align: center; color: #05A854; padding: 0px 0px;'" +
                ">UFSC em Dados</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px;'" +
                ">Atualização: 30/03/2023</h3>", unsafe_allow_html=True)
with col3:
    st.image(im)


st.markdown('---')

#df = df.astype(int)

selected_rows = agg_tabela(df, True)

tab1, tab2, tab3, tab4 = st.tabs(["‍🔬 LABORATÓRIO", "🔎 ANALISE EXPLORATÓRIA", "📊 DASHBOARD" , '👶 PRIMEIRA VEZ AQUI?'])

with tab1:
    if len(selected_rows) == 0:
        parte1(df, selected_rows)
    elif len(selected_rows) != 0:
        parte1(selected_rows, selected_rows)
with tab2:
    if len(selected_rows) == 0:
        relatorio(df)
    elif len(selected_rows) != 0:
        relatorio(selected_rows)
with tab3:
    st.text('Ainda Nada...')
with tab4:
    st.text('Ainda Nada...')


