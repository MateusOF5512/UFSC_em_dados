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

def bar_plot(df, var1, var2, cor1):


    values = df[var1]
    y = df[var2]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y, text=y, textposition='inside', insidetextanchor='start', name='',
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>"+var1+":</b> %{x}" +
                      "</br><b>"+var2+":</b> %{y}",
        marker_color=cor1))
    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        height=300, margin=dict(l=70, r=10, b=20, t=20), autosize=False,
        dragmode=False, hovermode="x", clickmode="event+select")
    fig.update_yaxes(
        title_text="Eixo Y - "+var2, title_font=dict(family='Sans-serif', size=14),
        tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3')
    fig.update_xaxes(
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    for figure in fig.data:
        figure.update(
            selected=dict(marker=dict(color="#E30613")),
            unselected=dict(marker=dict(color="#05A854", opacity=1)),
        )

    return fig


def bar_emp_plot(df, var0, var1, var2, var3, var4, var5, cor1, cor2, cor3, cor4, cor5, basedados, agrupamento):


    values = df[var0]
    y1 = df[var1]
    y2 = df[var2]
    y3 = df[var3]
    y4 = df[var4]
    y5 = df[var5]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y1, text=y1, textposition='inside', insidetextanchor='start', name=var1,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>"+var0+":</b> %{x}" +
                      "</br><b>"+agrupamento+":</b> %{y}",
        marker_color=cor1))
    fig.add_trace(go.Bar(
        x=values, y=y2, text=y2, textposition='inside', insidetextanchor='start', name=var2,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor2))
    fig.add_trace(go.Bar(
        x=values, y=y3, text=y3, textposition='inside', insidetextanchor='start', name=var3,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor3))
    fig.add_trace(go.Bar(
        x=values, y=y4, text=y4, textposition='inside', insidetextanchor='start', name=var4,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor4))
    fig.add_trace(go.Bar(
        x=values, y=y5, text=y5, textposition='inside', insidetextanchor='start', name=var5,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor5))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=10, orientation="h", yanchor="top", y=1.10, xanchor="center", x=0.35),
        height=300, margin=dict(l=80, r=10, b=20, t=20), autosize=False, barmode='stack',
        dragmode=False, clickmode="event+select"
    )
    fig.update_yaxes(
        title_text="Eixo Y - " + basedados + " por " + agrupamento, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3'
    )
    fig.update_xaxes(
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    for figure in fig.data:
        figure.update(
            selected=dict(marker=dict(color="#E30613")),
            unselected=dict(marker=dict(color="#05A854", opacity=1)),
        )

    return fig

def bar_group_plot(df, var0, var1, var2, var3, var4, var5, cor1, cor2, cor3, cor4, cor5, basedados, agrupamento):

    values = df[var0]
    y1 = df[var1]
    y2 = df[var2]
    y3 = df[var3]
    y4 = df[var4]
    y5 = df[var5]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=values, y=y1, text=y1, textposition='inside', insidetextanchor='start', name=var1,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>"+var0+":</b> %{x}" +
                      "</br><b>"+agrupamento+":</b> %{y}",
        marker_color=cor1))
    fig.add_trace(go.Bar(
        x=values, y=y2, text=y2, textposition='inside', insidetextanchor='start', name=var2,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor2))
    fig.add_trace(go.Bar(
        x=values, y=y3, text=y3, textposition='inside', insidetextanchor='start', name=var3,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor3))
    fig.add_trace(go.Bar(
        x=values, y=y4, text=y4, textposition='inside', insidetextanchor='start', name=var4,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor4))
    fig.add_trace(go.Bar(
        x=values, y=y5, text=y5, textposition='inside', insidetextanchor='start', name=var5,
        textfont=dict(size=20, color='white', family='Arial'), texttemplate='%{text:.3s}',
        hovertemplate="</br><b>" + var0 + ":</b> %{x}" +
                      "</br><b>" + agrupamento + ":</b> %{y}",
        marker_color=cor5))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=10, orientation="h", yanchor="top", y=1.10, xanchor="center", x=0.35),
        height=300, margin=dict(l=80, r=10, b=20, t=20), autosize=False, barmode='group',
        dragmode=False, clickmode="event+select"
    )
    fig.update_yaxes(
        title_text="Eixo Y - " + basedados + " por " + agrupamento, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3'
    )
    fig.update_xaxes(
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    for figure in fig.data:
        figure.update(
            selected=dict(marker=dict(color="#E30613")),
            unselected=dict(marker=dict(color="#05A854", opacity=1)),
        )

    return fig

def line_mult_plot(df, var0, var1, var2, var3, var4, var5, cor1, cor2, cor3, cor4, cor5, basedados, agrupamento):
    fig = go.Figure()

    values = df[var0]
    y1 = df[var1]
    y2 = df[var2]
    y3 = df[var3]
    y4 = df[var4]
    y5 = df[var5]

    fig.add_trace(go.Scatter(
        x=values, y=y1, name=var1,
        mode='lines+markers', hovertemplate=None, line=dict(width=3, color=cor1)))
    fig.add_trace(go.Scatter(
        x=values, y=y2, name=var2,
        mode='lines+markers', hovertemplate=None, line=dict(width=3, color=cor2)))
    fig.add_trace(go.Scatter(
        x=values, y=y3, name=var3,
        mode='lines+markers', hovertemplate=None, line=dict(width=3, color=cor3)))
    fig.add_trace(go.Scatter(
        x=values, y=y4, name=var4,
        mode='lines+markers', hovertemplate=None, line=dict(width=3, color=cor4)))
    fig.add_trace(go.Scatter(
        x=values, y=y5, name=var5,
        mode='lines+markers', hovertemplate=None, line=dict(width=3, color=cor5)))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=10, orientation="h", yanchor="top", y=1.05, xanchor="center", x=0.40),
        height=300, hovermode="x unified", autosize=False, dragmode=False, margin=dict(l=80, r=10, b=20, t=30)
    )
    fig.update_yaxes(
        title_text="Eixo Y - " + basedados + " por " + agrupamento, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3'
    )
    fig.update_xaxes(
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    return fig


def line_plot(df, varx, vary):
    fig = go.Figure()

    values = df[varx]
    y = df[vary]

    fig.add_trace(go.Scatter(
        x=values, y=y,
        mode='lines+markers', hovertemplate=None, line=dict(width=3, color='#05A854')))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=10, orientation="h", yanchor="top", y=1.10, xanchor="center", x=0.35),
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

def area(df, var0, var1, var2, var3, var4, var5, cor1, cor2, cor3, cor4, cor5, basedados, agrupamento):
    fig = go.Figure()

    values = df[var0]
    y1 = df[var1]
    y2 = df[var2]
    y3 = df[var3]
    y4 = df[var4]
    y5 = df[var5]

    fig.add_trace(go.Scatter(
        x=values, y=y1, name=var1,
        mode='lines+markers',
        line=dict(width=3, color=cor1),
        stackgroup='one',
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y2, name=var2,
        mode='lines+markers',
        line=dict(width=3, color=cor2),
        stackgroup='two'
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y3, name=var3,
        mode='lines+markers',
        line=dict(width=3, color=cor3),
        stackgroup='three'
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y4, name=var4,
        mode='lines+markers',
        line=dict(width=3, color=cor4),
        stackgroup='four'
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y5, name=var5,
        mode='lines+markers',
        line=dict(width=3, color=cor5),
        stackgroup='five'
    ))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=8, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=300, hovermode="x unified", autosize=False, dragmode=False, margin=dict(l=80, r=20, b=10, t=40)
    )
    fig.update_yaxes(
        title_text="Eixo Y - " + basedados + " por " + agrupamento, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=5, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3'
    )
    fig.update_xaxes(
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    return fig

def area_norm(df, var0, var1, var2, var3, var4, var5, cor1, cor2, cor3, cor4, cor5, basedados, agrupamento):
    fig = go.Figure()

    values = df[var0]
    y1 = df[var1]
    y2 = df[var2]
    y3 = df[var3]
    y4 = df[var4]
    y5 = df[var5]

    fig.add_trace(go.Scatter(
        x=values, y=y1, name=var1,
        mode='lines+markers',
        line=dict(width=3, color=cor1),
        stackgroup='one',
        groupnorm='percent'  # sets the normalization for the sum of the stackgroup
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y2, name=var2,
        mode='lines+markers',
        line=dict(width=3, color=cor2),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y3, name=var3,
        mode='lines+markers',
        line=dict(width=3, color=cor3),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y4, name=var4,
        mode='lines+markers',
        line=dict(width=3, color=cor4),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=values, y=y5, name=var5,
        mode='lines+markers',
        line=dict(width=3, color=cor5),
        stackgroup='one'
    ))

    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    fig.update_layout(
        paper_bgcolor="#F8F8FF", plot_bgcolor="#F8F8FF", font={'color': "#000000", 'family': "sans-serif"},
        legend=dict(font_size=8, orientation="h", yanchor="top", y=1.20, xanchor="center", x=0.5),
        height=300, hovermode="x unified", autosize=False, dragmode=False, margin=dict(l=80, r=20, b=10, t=40)
    )
    fig.update_yaxes(
        title_text="Eixo Y - " + basedados + " por " + agrupamento, title_font=dict(family='Sans-serif', size=12),
        tickfont=dict(family='Sans-serif', size=12), nticks=5, showgrid=True, gridwidth=0.5, gridcolor='#D3D3D3'
    )
    fig.update_xaxes(
        dtick=5, tickfont=dict(family='Sans-serif', size=12), nticks=10, showgrid=False
    )

    return fig