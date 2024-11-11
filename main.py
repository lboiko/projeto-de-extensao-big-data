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

st.sidebar.header("Filtragem dos dados:")

paises_selecionados = st.sidebar.multiselect(
    "Selecione o(s) país(es)", # título da seleção de países
    options=df['País de Origem'].unique(),
    default=[]
)

dados_filtrados = df[df['País de Origem'].isin(paises_selecionados)]

if paises_selecionados:
    
    st.sidebar.subheader("Seleção de Colunas")  # título da seção de colunas
    
    # Checkbox para selecionar/desmarcar todas as colunas
    selecionar_todas = st.sidebar.checkbox("Exibir todas as colunas", value=True)

    colunas_disponiveis = df.columns.tolist()
    
    # 
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
        st.write(f'### Dados filtrados para {paises_selecionados}', dados_filtrados)
    else:
        st.warning("Por favor, selecione ao menos uma coluna para exibir os dados.")
else:
    st.warning("Por favor, selecione ao menos um país.")

# Divisão em 3 colunas
if not dados_filtrados.empty:
        
        total_value = dados_filtrados['Valor total'].sum()
        total_peso = dados_filtrados['Peso total de cada peça'].sum()
        total_items = dados_filtrados.shape[0]
        
                
        # Métricas divididas por coluna
        col1, col2, col3 = st.columns([3, 5, 6])
        
        # with col1:
        #     st.metric(label="📦 Nº total de peças", value=f"{total_items}")
                    
        with col2:
            st.metric(label="💰 Valor total das peças", value=f"R$ {total_value:,.2f}")
        
        with col3:
            st.metric(label="⚖️ Peso total das peças", value=f"{total_peso:,.2f}kg")
            
st.markdown("---")

# Gráfico em barras
quantidade_por_categoria = dados_filtrados.groupby('País de Origem')['Quantidade Total de Itens'].sum().reset_index()

fig_quantidade = px.bar(quantidade_por_categoria, 
                        x='País de Origem', 
                        y='Quantidade Total de Itens',
                        title=f'Quantidade Total de Itens por País(es) - {paises_selecionados}')

# Eixo y - Quantidade
fig_quantidade.update_layout(
    width=800,  # Largura do gráfico
    height=700, # Altura do gráfico
    yaxis=dict(
        title='Quantidade Total de Itens',  
        tickmode='linear',   # modo dos ticks
        tick0=0,             # primeiro valor
        dtick=400,            # incremento
    )
)

st.plotly_chart(fig_quantidade)

st.markdown("---")

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
    dragmode = False, # sem arraste/zoom
    uirevision="fixed", # fixação do mapa
    template='plotly_dark',
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color="white",  # Cor do texto
    coloraxis_showscale=False,  # Sem a barra de cores do choropleth
    width=1200,  # largura
    height=800  # altura
)

st.plotly_chart(fig, use_container_width=False)
