import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel('dados/porsche_dados.xlsx', sheet_name='ITENS')

print(df.columns)
df.rename(columns={
    'id linha': 'ID',
    'CAT.': 'Categoria',
    'PROCESSO': 'Processo',
    'QNT': 'Quantidade Total de Itens',
    'DESCRIPTION': 'Descrição',
    'BRAND': 'Marca',
    'SERIAL No.': "Número de série",
    'MADE IN': 'País de Origem',
    'UNIT VALUE': 'Valor da unidade',
    'TOTAL VALUE': 'Valor total',
    'UNIT NET WEIGHT': 'Peso da unidade',
    'TOTAL NET WEIGHT': 'Peso total de cada peça'
}, inplace=True)

# Configuração da página
st.set_page_config(
    page_title="PORSCHE CUP - Dados e Logística",
    page_icon="⛴✈",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown( # Para deixar o fundo preto
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        .stApp {
            background-color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("PORSCHE CUP - Dados e Logística") #Título principal

# Barra lateral

st.sidebar.image(
    "./imagens/porschecuplogo.png",            
    width=300
)

st.sidebar.header("MENU DE FILTRAGEM DE DADOS:")

paises_selecionados = st.sidebar.multiselect(
    "Selecione o(s) país(es)", # título da seleção de países
    options=df['País de Origem'].unique(),
    default=[]
)

processo_pesquisado = st.sidebar.text_input("Digite o código do processo:")

dados_filtrados = df[df['País de Origem'].isin(paises_selecionados)] #verifica se os valores na coluna país de origem estão presentes na coleção paises_selecionados

if paises_selecionados:
    
    st.sidebar.subheader("Seleção de Colunas")  # título da seção de colunas
    
    # Checkbox para selecionar/desmarcar todas as colunas
    selecionar_todas = st.sidebar.checkbox("Exibir todas as colunas", value=True)

    colunas_disponiveis = df.columns.tolist()
    
    if selecionar_todas:
        colunas_selecionadas = colunas_disponiveis  # todas as colunas selecionadas
    else:
        # "Selecionar todas" desmarcada
        colunas_selecionadas = [
            coluna for coluna in colunas_disponiveis if st.sidebar.checkbox(coluna, value=True)
        ]
    
    if colunas_selecionadas:
        # Filtrar o DataFrame com base nas colunas selecionadas
        dados_filtrados = dados_filtrados[colunas_selecionadas]



        # Exibir os dados filtrados
        st.markdown(f"""
    <div style="background-color: #942525; padding: 5px; border-radius: 10px; color: white;">
        <h3>📄 Dados filtrados para: {', '.join(paises_selecionados)}</h3>
    </div>
""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.write(dados_filtrados)
    else:
        st.warning("Por favor, selecione ao menos uma coluna para exibir os dados.")
else:
    st.warning("Por favor, selecione ao menos um país.")

# Divisão em 2 colunas das métricas
if not dados_filtrados.empty:
        
        total_value = dados_filtrados['Valor total'].sum()
        total_peso = dados_filtrados['Peso total de cada peça'].sum()
        total_items = dados_filtrados.shape[0]
        
                
        # Métricas divididas por coluna
        col1, col2 = st.columns([1, 3])
                         
        with col1:
            st.metric(label="💰 Valor total das peças", value=f"R$ {total_value:,.2f}")
        
        with col2:
            st.metric(label="⚖️ Peso total das peças", value=f"{total_peso:,.2f}kg")
            
st.markdown("---")        

st.markdown(f"""
    <div style="background-color: #942525; padding: 5px; border-radius: 10px; color: white;"">
        <h3>{"📋 Itens filtrados por processo:"}</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# verifica se o processo foi digitado e exibe
if processo_pesquisado:
    try:               
        # filtra o df
        linha_encontrada = df[df["Processo"] == processo_pesquisado]

        # Exibir o resultado
        if not linha_encontrada.empty:
            st.dataframe(linha_encontrada)
        else:
            st.warning("Nenhum resultado encontrado para o processo informado.")
    except ValueError:
        st.error("Por favor, insira o código do processo.")

if processo_pesquisado:  
    
    dados_processo = df[df['Processo'].str.contains(processo_pesquisado, case=False, na=False)]
    
    if not dados_processo.empty:
        total_qnt_processo = dados_processo['Quantidade Total de Itens'].sum()  
        total_value_processo = dados_processo['Valor total'].sum()
        total_peso_processo = dados_processo['Peso total de cada peça'].sum()
        
        st.markdown(f"### Dados do Processo: {processo_pesquisado}")
        
        # métricas
        col1, col2, col3 = st.columns([2, 3, 4])
        
        with col1:
            st.metric(label="📦 Quantidade de peças", value=f"{total_qnt_processo:}")
        with col2:
            st.metric(label="💰 Valor total das peças", value=f"R$ {total_value_processo:,.2f}")
        
        with col3:
            st.metric(label="⚖️ Peso total das peças", value=f"{total_peso_processo:,.2f}kg")
         
st.markdown("---")

# Gráfico em barras
grafico_filtrados = df[df['País de Origem'].isin(paises_selecionados)] #verifica se os valores na coluna país de origem estão presentes na coleção paises_selecionados


st.markdown(f"""
    <div style="background-color: #942525; padding: 5px; border-radius: 10px; color: white;"">
        <h3>📊 Comparação de quantidade de itens por países: {', '.join(paises_selecionados)}</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

quantidade_por_categoria = grafico_filtrados.groupby('País de Origem')['Quantidade Total de Itens'].sum().reset_index()

fig_quantidade = px.bar(quantidade_por_categoria, 
                        x='País de Origem', 
                        y='Quantidade Total de Itens',
                        color='País de Origem'
                        
)

# Eixo y - Quantidade
fig_quantidade.update_layout(
    width=800,  
    height=700, 
    yaxis=dict(
        title='Quantidade Total de Itens',  
        tickmode='linear',   # modo dos ticks
        tick0=0,             # primeiro valor
        dtick=400,            # incremento
    )
)

st.plotly_chart(fig_quantidade)

st.markdown("---")

st.markdown(f"""
    <div style="background-color: #942525; padding: 5px; border-radius: 10px; color: white;"">
        <h3>🗺️ Países envolvidos na operação</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Mapa 
data = {
    "Country": ["Brazil", "Germany", "France",
        "United Kingdom", "Italy", "Austria"]
    
}

df = pd.DataFrame(data)

fig = px.choropleth(
    df,
    locations="Country", 
    locationmode="country names",  
    title="Mapa para melhor visualização:"
)

# Layout do mapa
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="black",
        showocean=True,
        oceancolor="black",
        projection_type="equirectangular",
        showframe=False,
        coastlinecolor="gray"
    ),
    dragmode = False, # arraste/zoom
    uirevision="fixed", # fixação do mapa
    template='plotly_dark',
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color="white",  # Cor do texto
    coloraxis_showscale=False,  # Sem a barra de cores do choropleth
    width=1200,  
    height=800  
)

st.plotly_chart(fig, use_container_width=False)
