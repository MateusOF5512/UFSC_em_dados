import sqlite3

import streamlit

from plots.plots import *

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import io



def sidebar_variaveis(df, grafico, basedados, agrupamento):
    with st.sidebar:
        if grafico == 'Barra Simples' or grafico == 'Linha Simples':
            col1, col2 = st.columns([1, 8])
            with col1:
                cor1 = st.color_picker('', '#05A854', key=1)
            with col2:
                df_y = df.drop('ANO', axis=1)
                vary_line = st.selectbox(agrupamento+' selecionado:', df_y.columns.unique(), index=0, key=2)
                varx_line = 'ANO'

        elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas' or \
                grafico == 'Multiplas Linhas' or grafico == 'Multiplas Áreas' or grafico == 'Área Normalizada':

            df['NULO'] = np.where(df['ANO'] == 0, 0, 0)
            cols = df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df = df[cols]

            df_y = df.drop('ANO', axis=1)

            col1, col2 = st.columns([1, 8])
            with col1:
                cor1 = st.color_picker('', '#05A854', key=31)
            with col2:
                vary_line1 = st.selectbox('1° '+agrupamento+' selecionado:', df_y.columns.unique(), index=1, key=32)

            col1, col2 = st.columns([1, 8])
            with col1:
                cor2 = st.color_picker('', '#005BAB', key=33)
            with col2:
                vary_line2 = st.selectbox('2° '+agrupamento+' selecionado:', df_y.columns.unique(), index=2, key=34)

            col1, col2 = st.columns([1, 8])
            with col1:
                cor3 = st.color_picker('', '#FFE400', key=35)
            with col2:
                vary_line3 = st.selectbox('3° '+agrupamento+' selecionado:', df_y.columns.unique(), index=0, key=36)

            col1, col2 = st.columns([1, 8])
            with col1:
                cor4 = st.color_picker('', '#ED1C24', key=37)
            with col2:
                vary_line4 = st.selectbox('4° '+agrupamento+' selecionado:', df_y.columns.unique(), index=0, key=38)

            col1, col2 = st.columns([1, 8])
            with col1:
                cor5 = st.color_picker('', '#F37519', key=39)
            with col2:
                vary_line5 = st.selectbox('5° '+agrupamento+' selecionado:', df_y.columns.unique(), index=0, key=40)

        st.markdown('---')

    if grafico == 'Linha Simples':
        fig1 = line_plot(df, varx_line, vary_line, cor1, agrupamento)
    elif grafico == 'Barra Simples':

        fig1 = bar_plot(df, varx_line, vary_line, cor1, agrupamento)

    elif grafico == 'Barras Empilhadas':
        fig1 = bar_emp_plot(df, 'ANO', vary_line1, vary_line2, vary_line3, vary_line4, vary_line5,
                            cor1, cor2, cor3, cor4, cor5, basedados, agrupamento)

    elif grafico == 'Barras Agrupadas':
        fig1 = bar_group_plot(df, 'ANO', vary_line1, vary_line2, vary_line3, vary_line4, vary_line5,
                              cor1, cor2, cor3, cor4, cor5, basedados, agrupamento)
    elif grafico == 'Multiplas Linhas':
        fig1 = line_mult_plot(df, 'ANO', vary_line1, vary_line2, vary_line3, vary_line4, vary_line5,
                              cor1, cor2, cor3, cor4, cor5, basedados, agrupamento)
    elif grafico == 'Multiplas Áreas':
        fig1 = area(df, 'ANO', vary_line1, vary_line2, vary_line3, vary_line4, vary_line5,
                              cor1, cor2, cor3, cor4, cor5, basedados, agrupamento)
    elif grafico == 'Área Normalizada':
        fig1 = area_norm(df, 'ANO', vary_line1, vary_line2, vary_line3, vary_line4, vary_line5,
                              cor1, cor2, cor3, cor4, cor5, basedados, agrupamento)

    max = str(df['ANO'].max())
    min = str(df['ANO'].min())

    if basedados == "População Universitária":

        if grafico == 'Barra Simples' or grafico == 'Linha Simples':
            st.markdown("<h3 style='font-size:125%; text-align: center; color: #05A854; padding: 10px 0px 0px 0px;'" +
                        "><b>" + basedados + "</b>: n° de <b>" + agrupamento + " - análise temporal | " + min +
                        " - " + max + " | " + grafico + "</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px;'" +
                        "><b>" + agrupamento + " selecionado:</b> " + vary_line + "</p>", unsafe_allow_html=True)

        elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas' or \
                grafico == 'Multiplas Áreas' or grafico == 'Área Normalizada':
            st.markdown("<h3 style='font-size:125%; text-align: center; color: #05A854; padding: 10px 0px 0px 0px;'" +
                        "><b>" + basedados + "</b>: n° de <b>" + agrupamento + " - análise temporal | " + min +
                        " - " + max + " | "+grafico+"</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px;'" +
                        "><b>" + agrupamento + " selecionado:</b> " + vary_line1 + ",  "+vary_line2+
                        ",  "+vary_line3+",  "+vary_line4+" e  "+vary_line5+"</p>", unsafe_allow_html=True)

    elif basedados == "Vagas no Vestibular":

        if grafico == 'Barra Simples' or grafico == 'Linha Simples':
            st.markdown("<h3 style='font-size:125%; text-align: center; color: #05A854; padding: 10px 0px 0px 0px;'" +
                        "><b>" + basedados + "</b>: n° por <b>" + agrupamento + " - análise temporal | " + min +
                        " - " + max + " | " + grafico + "</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px;'" +
                        "><b>" + agrupamento + " selecionado:</b> " + vary_line + "</p>", unsafe_allow_html=True)

        elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas' or \
                grafico == 'Multiplas Áreas' or grafico == 'Área Normalizada':
            st.markdown("<h3 style='font-size:125%; text-align: center; color: #05A854; padding: 10px 0px 0px 0px;'" +
                        "><b>" + basedados + "</b>: n° por <b>" + agrupamento + " - análise temporal | " + min +
                        " - " + max + " | " + grafico + "</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px;'" +
                        "><b>" + agrupamento + " selecionado:</b> " + vary_line1 + ",  " + vary_line2 +
                        ",  " + vary_line3 + ",  " + vary_line4 + " e  " + vary_line5 + "</p>",unsafe_allow_html=True)

    if grafico == 'Barra Simples' or grafico == 'Linha Simples':
        return fig1, varx_line, vary_line

    elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas' or \
            grafico == 'Multiplas Linhas' or grafico == 'Multiplas Áreas' or grafico == 'Área Normalizada':
        return fig1, vary_line1, vary_line2, vary_line3, vary_line4, vary_line5



##############################################################################################################
# LAYOUT DAS BASES DE DADOS:
##############################################################################################################

def populacao(df, selected_rows, grafico, basedados, agrupamento):


    if grafico == 'Barra Simples' or grafico == 'Linha Simples':
        fig1, varx_line, vary_line = sidebar_variaveis(df, grafico, basedados, agrupamento)

    elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas' or \
            grafico == 'Multiplas Linhas' or grafico == 'Multiplas Áreas' or grafico == 'Área Normalizada':
        fig1, vary_line1, vary_line2, vary_line3, vary_line4, vary_line5 = sidebar_variaveis(df, grafico, basedados, agrupamento)

    st.plotly_chart(fig1, use_container_width=True, config=config)

    max = str(df['ANO'].max())
    min = str(df['ANO'].min())

    if grafico == 'Barra Simples' or grafico == 'Linha Simples':

        with st.expander("Análise descritiva guiada por modelo de linguagem de inteligência artificial 🤖"):

            st.markdown("<h3 style='font-size:130%; text-align: center; color: #05A854; font:'sans serif';" +
                        ">Configure o ChatGPT-3 para análisar os dados: <br>"+vary_line+" entre "+min+" e "+max+"</h3>", unsafe_allow_html=True)

            if len(selected_rows) == 0:
                prompt2 = (
                        f"Os dados do gráfico são uma analise tempotal de " + min + " até " + max +
                        f" de informações sobre a Universidade Federal de Santa Catarina - Brasil.\n"
                        f"Dados do gráfico: {df[[varx_line, vary_line]].to_string(index=False)}, "
                        f"o contexto da informações é a {basedados} de {agrupamento}  com número de: {vary_line}.\n"
                        f"Elabore o resumo com base nos Dados disponibilizados observando cada década e suas métricas:\n")
            elif len(selected_rows) != 0:
                prompt2 = (
                        f"Os dados do gráfico são uma analise tempotal de " + min + " até " + max +
                        f" de informações sobre a Universidade Federal de Santa Catarina - Brasil.\n"
                        f"Dados do gráfico: {df[[varx_line, vary_line]].to_string(index=False)}, "
                        f"o contexto da informações é a {basedados} de {agrupamento}  com número de: {vary_line}.\n"
                        f"Elabore o resumo com base nos Dados disponibilizados observando cada ANO e suas métricas:\n")

            col1, col2 = st.columns([2, 2])
            with col1:
                api_key = st.text_input('Adicione sua API Key | OpenAI:')
            with col2:
                temperature = st.slider('Regule a criatividade do ChatGPT3:',
                                        min_value=0.1, max_value=1.0, value=0.8, step=0.1, key=10)
            st.markdown('---')

            if len(api_key) == 0:
                st.warning(
                    'Para visualizar as informações geradas pelo ChatGPT-3, é necessário adicionar sua API-Key '
                    'na caixa de texto localizada na parte superior da tela. Caso ainda não tenha uma chave de API, '
                    'você pode criá-la acessando o seguinte endereço: https://platform.openai.com/account/api-keys.',
                    icon='🗝️')
            elif len(api_key) != 0:
                summary2 = generate_summary(prompt2, temperature, api_key)
                st.markdown("<h3 style='font-size:120%; text-align: center; color: #05A854;'" +
                            ">Análise descritiva dos dados apresentados no gráfico</h3>", unsafe_allow_html=True)

                st.write(summary2)
                st.markdown('---')

                if len(selected_rows) == 0:
                    solicitacao = st.text_area('Faça uma pergunta sobre os dados apresentados no gráfico:',
                                               'Exemplo: qual a variação percentual a cada década?', key="placeholder")

                elif len(selected_rows) != 0:
                    solicitacao = st.text_area('Faça uma pergunta sobre os dados apresentados no gráfico:',
                                               'Exemplo: qual a variação percentual a cada ano?', key="placeholder")

                if len(api_key) != 0 and len(solicitacao) != 0:
                    prompt3 = (
                        f"Dados do DataFrame: {df[[varx_line, vary_line]].to_string(index=False)}.\n"
                        f"Usando os Dados resolva a pergunta: {solicitacao}:\n"
                        f"Resposta final apresente uma tabela em markdown com a solução da pergunta:\n")
                    summary3 = generate_summary(prompt3, temperature, api_key)
                    st.write(summary3)

            st.markdown('---')

        with st.expander("Conferir Dados do Gráfico 🔎️ "):
            df_barra = df[[varx_line, vary_line]]

            checkdf = st.checkbox('Visualizar Dados', key=70)
            if checkdf:
                st.markdown("<h3 style='font-size:100%; text-align: center; color: #05A854;'" +
                            "><i>Analise Temporal " + min + " a " + max + ": " + vary_line + "</i> - TABELA RESUMIDA</h3>",
                            unsafe_allow_html=True)
                agg_tabela(df_barra, use_checkbox=False)

            df_barra = df_barra.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Dados", data=df_barra,
                               file_name="Analise_Temporal_" + min + "_" + max + "_" + vary_line + ".csv", mime='csv')

    elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas':
        with st.expander("Análise descritiva gerada por Inteligencia Artificial 🤖"):

            st.markdown('Em construção...')

            st.markdown('---')


        with st.expander("Conferir Dados do Gráfico 🔎️ "):
            df_barra = df[['ANO', vary_line1,vary_line2,vary_line3,vary_line4,vary_line5 ]]

            checkdf = st.checkbox('Visualizar Dados', key=71)
            if checkdf:

                agg_tabela(df_barra, use_checkbox=False)

            df_barra = df_barra.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Dados", data=df_barra,
                               file_name="Analise_Temporal_"+min+"_"+max+"_"+basedados+"_"+agrupamento+".csv", mime='csv')


    return None



def relatorio(df, basedados, agrupamento):

    st.markdown("<h3 style='font-size:150%; text-align: center; color: #05A854; padding: 20px 0px 0px 0px;'" +
                ">Relatório Básico sobre a Tabela selecionada:</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:120%; text-align: center; color: #05A854; padding: 0px 0px 0px 0px;'" +
                ">"+basedados+" agrupapados por tipo de "+agrupamento+"</p>", unsafe_allow_html=True)
    st.markdown('---')

    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()

    df_des = df.describe()


    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("<h4 style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 10px 0px;'" +
                    ">Variáveis, seus Tipos e Memória</h4>", unsafe_allow_html=True)
        st.text(s)
    with col2:
        st.markdown("<h4 style='font-size:100%; text-align: center; color: #05A854; padding: 0px 0px 10px 0px;'" +
                    ">Estatísticas Básicas</h4>", unsafe_allow_html=True)
        st.dataframe(df_des)
    st.markdown('---')

    text = """Para gerar o relatório, utilizamos o pandas-profiling, uma ferramenta que proporciona uma análise 
    profunda, rápida e simples dos dados. Essa ferramenta gera automaticamente relatórios personalizados para cada 
    variável do conjunto de dados, apresentando estatísticas, gráficos, alertas, correlações e outras informações 
    relevantes. É importante ressaltar que o tempo de geração dos relatórios pode variar de alguns segundos a alguns 
    minutos, dependendo do tamanho da tabela."""


    st.markdown("<h3 style='font-size:150%; text-align: center; color: #05A854; padding: 20px 0px 0px 0px;'" +
                ">Relatório Avançado - Exploratory Data Analysis (EDA) com Pandas profiling:</h3>", unsafe_allow_html=True)
    st.markdown('---')

    col1, col2 = st.columns([2, 10])
    with col1:
        st.text('')
        st.text('')
        st.text('')
        report = st.checkbox("🔎 Carregar relatório avançado: ", key=41)
    with col2:
        st.info(text)
    st.markdown('---')

    if report:
        profile = ProfileReport(df, title="Relatório dos Dados", explorative=True)
        st_profile_report(profile)

    return None


def rodape():
    html_rodpe = """
    <hr style= "display: block;
      margin-top: 0.5em;
      margin-bottom: 0.5em;
      margin-left: auto;
      margin-right: auto;
      border-style: inset;
      border-width: 1.5px;">
      <p style="color:#05A854; text-align: center;">Última atualização: 25/04/23 | mateus7ortiz@gmail.com</p>
    """
    st.markdown(html_rodpe, unsafe_allow_html=True)


    return None


def boasvindas():
    st.markdown(
        "<p style='font-size:100%; text-align: justify; color: #000000; padding: 0px 0px 0px 0px;'" +
        ">Nosso aplicativo web é desenvolvido com <a href='https://streamlit.io/gallery' target='_blank'>Streamlit</a>, "
        "que é uma biblioteca de código aberto em <a href='https://pt.wikipedia.org/wiki/Python' target='_blank'>Python</a> "
        "projetada para ajudar os desenvolvedores a criar aplicativos web interativos de maneira fácil e rápida. "
        "Sendo uma ferramenta extremamente útil para a criação de aplicativos web de machine learning e análise de " 
        "dados. Com sua interface amigável e recursos interativos, o Streamlit torna mais fácil do que nunca criar "
        "aplicativos que permitem aos usuários explorar e visualizar seus dados de maneira intuitiva e eficiente.</p>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size: 100%; text-align: justify; color: #000000; padding: 0px 0px 0px 0px;'" +
        ">Para apresentar o <a href='https://dpgi-seplan.ufsc.br/boletim-de-dados/' target='_blank'>Boletim de dados da UFSC</a>, "
        "usamos tabelas dinâmicas com Ag Grid e gráficos interativos com Plotly Express. "
        "A biblioteca <a href='https://www.ag-grid.com/' target='_blank'>Ag Grid</a> é uma ferramenta poderosa "
        "para a criação de tabelas interativas e dinâmicas, "
        "permitindo que os usuários filtrem, ordenem, classifiquem e pesquisem dados de maneira eficiente. "
        "Com <a href='https://plotly.com/python/plotly-express/' target='_blank'>Plotly Express</a>, "
        "podemos criar gráficos interativos que permitem aos usuários explorar os dados de diferentes "
        "perspectivas. Os gráficos podem ser manipulados pelos usuários, permitindo que "
        "realizem zoom, movimentação pelos eixos, seleção de diferentes áreas dos gráficos e download. Isso torna "
        "mais fácil para os usuários explorar os dados em detalhes e extrair insights valiosos.</p>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:100%; text-align: justify; color: #000000; padding: 0px 0px 0px 0px;'" +
        ">Além disso, utilizamos métodos de exploração e visualização de dados para fornecer aos usuários "
        "insights valiosos sobre os dados da UFSC. Para tornar a análise de dados ainda mais eficiente, "
        "também incluímos análises descritivas geradas automaticamente pela "
        "<a href='https://platform.openai.com/overview' target='_blank'>API do ChatGPT-3</a>. "
        "Essas análises fornecem uma compreensão mais aprofundada dos dados e ajudam os usuários a tirar conclusões com mais informações. "
        "Além disso, os usuários podem fazer perguntas sobre os dados e receber respostas em forma de tabelas, "
        "fornecendo ainda mais insights valiosos.</p>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:100%; text-align: justify; color: #000000; padding: 0px 0px 0px 0px;'" +
        ">Em resumo, nosso aplicativo web utiliza uma combinação de tecnologias avançadas para fornecer uma "
        "plataforma fácil de usar e eficiente para a análise e exploração de dados da UFSC. Com nossas ferramentas"
        " de visualização, filtragem e análise, os usuários podem explorar informações de maneira mais intuitiva e "
        "extrair insights valiosos para suas pesquisas e projetos.</p>", unsafe_allow_html=True)


    st.text("")

    st.markdown(
        "<h3 style='font-size:100%; text-align: justify; color: #05A854; padding: 0px 0px 0px 0px;'" +
        ">LABORATÓRIO 🔬 :</h3>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:90%; text-align: justify; color: #000000; padding: 0px 0px 0px 0px;'" +
        ">Com o Laboratório o usuário pode realizar suas experiências, gerar e comprovar insights, manipulando todas "
        "as variáveis dos dados em diferentes formas e perspectivas. O laboratório é a nossa ferramenta mais poderosa, "
        "simplificando a análise intuitiva do usuário e fornecendo análises descritivas geradas por inteligência artificial "
        "para complemento. Suas principais funcionalidades são:</p>", unsafe_allow_html=True)

    st.markdown("<ul> "
                "<li style='font-size:90%; color: #000000; margin-top: -5px;'>Análise e visualização de todas as colunas da base de dados</li>"
                "<li style='font-size:90%; color: #000000; margin-top: -5px'>Manipilação dos eixos dos gráficos</li>"
                "<li style='font-size:90%; color: #000000; margin-top: -5px'>Manipulação dos tipos de gráficos</li>"
                "<li style='font-size:90%; color: #000000; margin-top: -5px'>Análise gerada por Inteligencia Artificial</li>"
                "<li style='font-size:90%; color: #000000; margin-top: -5px'>Download dos gráficos e seus dados</li>"
                "</ul>", unsafe_allow_html=True)



    return None


def vagasvestibular(df, selected_rows, grafico, basedados, agrupamento):
    if grafico == 'Barra Simples' or grafico == 'Linha Simples':
        fig1, varx_line, vary_line = sidebar_variaveis(df, grafico, basedados, agrupamento)

    elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas' or \
            grafico == 'Multiplas Linhas' or grafico == 'Multiplas Áreas' or grafico == 'Área Normalizada':
        fig1, vary_line1, vary_line2, vary_line3, vary_line4, vary_line5 = sidebar_variaveis(df, grafico, basedados,
                                                                                             agrupamento)

    st.plotly_chart(fig1, use_container_width=True, config=config)

    max = str(df['ANO'].max())
    min = str(df['ANO'].min())

    if grafico == 'Barra Simples' or grafico == 'Linha Simples':
        with st.expander("Análise descritiva gerada por Inteligencia Artificial 🤖"):
            st.markdown("<h3 style='font-size:100%; text-align: center; color: #05A854; font:'sans serif';" +
                        ">Configure o ChatGPT-3 para análisar os dados: <br>"+vary_line+" entre "+min+" e "+max+"</h3>", unsafe_allow_html=True)


            if len(selected_rows) == 0:
                prompt = (
                    f"Os dados do gráfico são uma analise tempotal de "+min+" até "+max+" de informações sobre a Universidade Federal de Santa Catarina - Brasil.\n"
                    f"Dados do gráfico: {df[[varx_line, vary_line]].to_string(index=False)}, "
                    f"o contexto da informações é a {basedados} de {agrupamento}  com número de: {vary_line}.\n"
                    f"Elabore o resumo com base nos Dados disponibilizados observando cada década e suas métricas:\n")
            elif len(selected_rows) != 0:
                prompt = (
                    f"Os dados do gráfico são uma analise tempotal de "+min+" até "+max+" de informações sobre a Universidade Federal de Santa Catarina - Brasil.\n"
                    f"Dados do gráfico: {df[[varx_line, vary_line]].to_string(index=False)}, "
                    f"o contexto da informações é a {basedados} de {agrupamento}  com número de: {vary_line}.\n"
                    f"Elabore o resumo com base nos Dados disponibilizados observando cada ANO e suas métricas:\n")

            col1, col2 = st.columns([2, 2])
            with col1:
                api_key = st.text_input('Adicione sua API Key | OpenAI:')
            with col2:
                temperature = st.slider('Regule a criatividade do ChatGPT:',
                                        min_value=0.1, max_value=1.0, value=0.8, step=0.1, key=51)
            st.markdown('---')

            if len(api_key) == 0:
                st.warning('Para visualizar as informações geradas pelo ChatGPT-3, é necessário adicionar sua API-Key na caixa de texto localizada na parte superior da tela. '
                        'Caso ainda não tenha uma chave de API, você pode criá-la acessando o seguinte endereço: https://platform.openai.com/account/api-keys.',
                        icon='🗝️')
            elif len(api_key) != 0:
                summary2 = generate_summary(prompt, "text-davinci-003", temperature, api_key)
                st.markdown("<h3 style='font-size:120%; text-align: center; color: #05A854;'" +
                            ">Análise descritiva dos dados apresentados no gráfico</h3>", unsafe_allow_html=True)

                st.write(summary2)
                st.markdown('---')

                if len(selected_rows) == 0:
                    solicitacao = st.text_area('Faça uma pergunta sobre os dados apresentados no gráfico:',
                                                'Exemplo: qual a variação percentual a cada década?', key="placeholder")

                elif len(selected_rows) != 0:
                    solicitacao = st.text_area('Faça uma pergunta sobre os dados apresentados no gráfico:',
                                                'Exemplo: qual a variação percentual a cada ano?', key="placeholder")

                if len(api_key) != 0 and len(solicitacao) != 0:
                    prompt3 = (
                        f"Dados do DataFrame: {df[[varx_line, vary_line]].to_string(index=False)}.\n"
                        f"Usando os Dados resolva a pergunta: {solicitacao}:\n"
                        f"Resposta final apresente uma tabela em markdown com a solução da pergunta:\n")
                    summary3 = generate_summary(prompt3, "text-davinci-003", temperature, api_key)
                    st.write(summary3)

            st.markdown('---')

        with st.expander("Conferir Dados do Gráfico 🔎️ "):
            df_barra = df[[varx_line, vary_line]]

            checkdf = st.checkbox('Visualizar Dados', key=50)
            if checkdf:
                st.markdown("<h3 style='font-size:100%; text-align: center; color: #05A854;'" +
                            "><i>Analise Temporal " + min + " a " + max + ": " + vary_line + "</i> - TABELA RESUMIDA</h3>",
                            unsafe_allow_html=True)
                agg_tabela(df_barra, use_checkbox=False)

            df_barra = df_barra.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Dados", data=df_barra,
                               file_name="Analise_Temporal_" + min + "_" + max + "_" + vary_line + ".csv", mime='csv')


    elif grafico == 'Barras Empilhadas' or grafico == 'Barras Agrupadas' or \
            grafico == 'Multiplas Linhas' or grafico == 'Multiplas Áreas' or grafico == 'Área Normalizada':
        with st.expander("Análise descritiva gerada por Inteligencia Artificial 🤖"):

            st.markdown('Em construção...')

            st.markdown('---')


        with st.expander("Conferir Dados do Gráfico 🔎️ "):

            v5 = df[vary_line5].sum()
            v4 = df[vary_line4].sum()
            v3 = df[vary_line3].sum()
            v2 = df[vary_line2].sum()
            v1 = df[vary_line1].sum()

            if v5 > 0 and v4 > 0 and v3 > 0 and v2 > 0 and v1 > 0:
                df_barra = df[['ANO', vary_line1, vary_line2, vary_line3, vary_line4, vary_line5]]
            elif v4 > 0 and v3 > 0 and v2 > 0 and v1 > 0:
                df_barra = df[['ANO', vary_line1, vary_line2, vary_line3, vary_line4]]
            elif v3 > 0 and v2 > 0 and v1 > 0:
                df_barra = df[['ANO', vary_line1, vary_line2, vary_line3]]
            elif v2 > 0 and v1 > 0:
                df_barra = df[['ANO', vary_line1, vary_line2]]
            elif v1 > 0:
                df_barra = df[['ANO', vary_line1]]

            checkdf = st.checkbox('Visualizar Dados do Gráfico', key=71)
            if checkdf:

                agg_tabela(df_barra, use_checkbox=False)

            df_barra = df_barra.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Dados", data=df_barra,
                               file_name="Analise_Temporal_"+min+"_"+max+"_"+basedados+"_"+agrupamento+".csv", mime='csv')










    return None