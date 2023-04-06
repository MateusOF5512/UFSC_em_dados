import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from PIL import Image

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai

@st.cache
def load_google_sheet(tabela):
    # Autenticação do Google
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('dados/streamlit-373718-f2e709f0d5bc.json', scope)
    client = gspread.authorize(creds)

    # Carregar a planilha do Google Sheets
    url = 'https://docs.google.com/spreadsheets/d/1cWZ5Pn5ELyH95KgTCNzMJexmPAgGQ9QdWz1x5pfy9ek/edit?usp=sharing'
    sheet = client.open_by_url(url).worksheet(tabela)

    # Converter os dados da planilha em um DataFrame do Pandas
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)



    return df

def tratamento1(df):
    df = df.astype(int)

    return df


def tratamento2(df):
    df = df.replace("-", 0)
    df2 = df[['1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990',
            '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
            '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
            '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
            '2018', '2019', '2020', '2021']].apply(pd.to_numeric, downcast='integer', errors='coerce')

    df[df2.columns] = df2

    return df

def generate_summary(prompt, engine, temperature, api_key):
    openai.api_key = api_key

    max_context_length = 2049  # tamanho máximo do contexto do GPT-3
    max_completion_length = 1024  # tamanho máximo para a conclusão

    if len(prompt) > max_context_length:
        prompt = prompt[:max_context_length]

    if max_completion_length > 1024:
        max_completion_length = 1024

    completion = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_completion_length,
        n=1,
        stop=None,
        temperature=temperature,
    )

    if len(completion.choices[0].text) > max_completion_length:
        completion.choices[0].text = completion.choices[0].text[:max_completion_length]

    return completion.choices[0].text




def agg_tabela(df, use_checkbox):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=False)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                    aggFunc="sum", editable=True)
    gb.configure_selection(use_checkbox=use_checkbox, selection_mode='multiple')
    gb.configure_side_bar()
    gridoptions = gb.build()
    df_grid = AgGrid(df, gridOptions=gridoptions, enable_enterprise_modules=True,
                     update_mode=GridUpdateMode.SELECTION_CHANGED, height=300, width='100%')
    selected_rows = df_grid["selected_rows"]
    selected_rows = pd.DataFrame(selected_rows)

    return selected_rows


config={"displayModeBar": True,
        "displaylogo": False,
        'modeBarButtonsToRemove': ['toggleSpikelines', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian']}

def bar_plot(df, var1, var2):


    values = df[var1]
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, text=y, textposition='inside', insidetextanchor='start', name='',
        textfont=dict(size=20, color='white', family='Arial'),
        hovertemplate="</br><b>"+var1+":</b> %{x}" +
                      "</br><b>"+var2+":</b> %{y}",
        marker_color='#05A854'))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=70, r=10, b=20, t=20), autosize=False,
        dragmode=False, hovermode="x", clickmode="event+select")
    fig.update_yaxes(
        title_text="Eixo Y - "+var2, title_font=dict(family='Sans-serif', size=14),
        tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')
    fig.update_xaxes(
        title_text="Eixo X - "+var1, title_font=dict(family='Sans-serif', size=14), dtick=5,
        tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False)

    for figure in fig.data:
        figure.update(
            selected=dict(marker=dict(color="#E30613")),
            unselected=dict(marker=dict(color="#05A854", opacity=1)),
        )

    return fig


def line_plot(df, varx, vary):
    fig = go.Figure()

    values = df[varx]
    y = df[vary]

    fig.add_trace(go.Scatter(
        x=values, y=y,
        mode='lines', hovertemplate=None, line=dict(width=3, color='#05A854')))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, hovermode="x unified", autosize=False, dragmode=False, margin=dict(l=80, r=10, b=20, t=10)
    )
    fig.update_xaxes(
        title_text="Eixo X: "+varx, title_font=dict(family='Sans-serif', size=18), dtick=5,
        tickfont=dict(family='Sans-serif', size=12),  showgrid=False, rangeslider_visible=False,
    )
    fig.update_yaxes(
        title_text="Eixo Y: "+vary, title_font=dict(family='Sans-serif', size=18),
        tickfont=dict(family='Sans-serif', size=12), nticks=7, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3'
    )

    return fig




