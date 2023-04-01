import streamlit

from plots.plots import *

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


def parte1(df, selected_rows):
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        df_x = df[['ANO']]
        varx_line = st.selectbox('Coluna Eixo X:', df_x.columns.unique(), index=0, key=1)
    with col1:
        df_y = df.drop('ANO', axis=1)
        vary_line = st.selectbox('Coluna Eixo Y:', df_y.columns.unique(), index=1, key=2)
    with col3:
        grafico = st.selectbox('Tipo do Gráfico:', ['Barra', 'Linha', 'Bolha' ], index=0, key=3)

    if grafico == 'Linha':
        fig1 = line_plot(df, varx_line, vary_line)

    elif grafico == 'Barra':
        fig1 = bar_plot(df, varx_line, vary_line)

    max = str(df[varx_line].max())
    min = str(df[varx_line].min())

    st.markdown('---')
    st.markdown("<h2 style='font-size:150%; text-align: center; color: #05A854; padding: 0px 0px;'" +
                ">Analise Temporal "+min+" a "+max+": "+vary_line+"</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 10px 0px;'" +
                ">Dados: " + str(df.shape[0]) + " anos</h4>", unsafe_allow_html=True)

    st.plotly_chart(fig1, use_container_width=True, config=config)



    with st.expander("Análise Descritiva: ChatGPT3 🤖"):

        st.subheader("Resumo dos Gráfico:")

        if len(selected_rows) == 0:
            prompt2 = (
                f"Os dados do gráfico são uma analise tempotal de "+min+" até "+max+" de informações sobre a Universidade Federal de Santa Catarina - Brasil.\n"
                f"Dados do gráfico: {df[[varx_line, vary_line]].to_string(index=False)}, e a informações é o número de: {vary_line}.\n"
                f"Elabore o resumo com base nos Dados disponibilizados observando cada década e suas métricas:\n")
        elif len(selected_rows) != 0:
            prompt2 = (
                f"Os dados do gráfico são uma analise tempotal de "+min+" até "+max+" de informações sobre a Universidade Federal de Santa Catarina - Brasil.\n"
                f"Dados do gráfico: {df[[varx_line, vary_line]].to_string(index=False)}, e a informações é o número de: {vary_line}.\n"
                f"Elabore o resumo com base nos Dados disponibilizados observando cada ANO e suas métricas:\n")

        col1, col2 = st.columns([2, 2])
        with col1:
            api_key = st.text_input('Adiicione sua API-Key:', value='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')
        with col2:
            temperature = st.slider('Regule a criatividade do Modelo:',
                                    min_value=0.1, max_value=1.0, value=0.8, step=0.1, key=10)

        if len(api_key) == 0:
            st.write('Adicione uma API-key -> para criar uma acesse: https://platform.openai.com/account/api-keys')
        elif len(api_key) != 0:
            summary2 = generate_summary(prompt2, "text-davinci-003", temperature, api_key)
            st.write(summary2)

        st.markdown('---')

    with st.expander("Conferir Dados do Gráfico 🔎️ "):
        df_barra = df[[varx_line, vary_line]]

        checkdf = st.checkbox('Visualizar Dados', key=70)
        if checkdf:

            st.markdown("<h3 style='font-size:100%; text-align: center; color: #05A854;'" +
                        "><i>Analise Temporal "+min+" a "+max+": "+vary_line+"</i> - TABELA RESUMIDA</h3>", unsafe_allow_html=True)
            agg_tabela(df_barra, use_checkbox=False)

        df_barra = df_barra.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download Dados", data=df_barra,
                           file_name="Analise_Temporal_"+min+"_"+max+"_"+vary_line+".csv", mime='csv')


    return None


def relatorio(df):

    st.markdown('---')
    st.markdown("<h3 style='font-size:200%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px;'" +
                ">Análise Exploratória dos Dados</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size:120%; text-align: center; color: #05A854; padding: 0px 0px;'" +
                ">Dados em Análise: " + str(df.shape[0]) + "</h4>", unsafe_allow_html=True)
    st.markdown('---')

    text = """Para gerar os Relatórios utilizamos o pandas-profiling, que entrega todas as ferramentas necessárias para 
                    uma análise profunda, rápida e simples dos dados. Gerando automaticamente relatórios personalizados para 
                    cada variável no conjunto de dados, com estatística, gráficos, alertas, correlações e mais. 
                    Para gerar esses Relatórios pode demorar uns segundos, dependendo da Tabela até minutos."""

    st.info(text)



    report = st.checkbox("🔎 Carregar Análise Exploratória dos Dados: ", key=40)

    if report:
        profile = ProfileReport(df, title="Relatório dos Dados", explorative=True)
        st_profile_report(profile)

    return None