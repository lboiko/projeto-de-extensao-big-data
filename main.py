import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import requests


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

st.title("PORSCHE CUP - Dados e Logistica") #Título principal

st.sidebar.image(
    "./imagens/porschecuplogo.png",            
    width=300
)

# Barra lateral
st.sidebar.header("Filtragem")


paises_selecionados = st.sidebar.multiselect(
    "Selecione o(s) país(es)",
    options=df['País de Origem'].unique(),
    default=[]
)

#Aplicar filtros ao dataset

dados_filtrados = df[(df['País de Origem'].isin(paises_selecionados))]
                       

#Exibir dados filtrados
st.write(f'### Dados filtrados para {paises_selecionados}', dados_filtrados)


# 3 colunas de dados abaixo da tabela 

if not dados_filtrados.empty:
        
        total_value = dados_filtrados['Valor total'].sum()
        total_peso = dados_filtrados['Peso total de cada peça'].sum()
        total_items = dados_filtrados.shape[0]
        
                
        # Métricas divididas por coluna
        col1, col2, col3 = st.columns([3, 5, 6])
        
        with col1:
            st.metric(label="📦 Nº total de peças", value=f"{total_items}")
                    
        with col2:
            st.metric(label="💰 Valor total das peças", value=f"R$ {total_value:,.2f}")
        
        with col3:
            st.metric(label="⚖️ Peso total das peças", value=f"{total_peso:,.2f}kg")
            
st.markdown("---")

# gráfico em barras
quantidade_por_categoria = dados_filtrados.groupby('País de Origem')['Quantidade Total de Itens'].sum().reset_index()

fig_quantidade = px.bar(quantidade_por_categoria, 
                        x='País de Origem', 
                        y='Quantidade Total de Itens',
                        title=f'Quantidade Total de Itens por País(es) - {paises_selecionados}')

# Eixo y - Quantidade
fig_quantidade.update_layout(
    width=1000,  # Largura do gráfico
    height=800, # Altura do gráfico
    yaxis=dict(
        title='Quantidade Total de Itens',  
        tickmode='linear',   # modo dos ticks
        tick0=0,             # primeiro valor
        dtick=400,            # incremento
    )
)

st.plotly_chart(fig_quantidade)

st.markdown("---")

# Mapa dos países de origem e destino

mapa = folium.Map(location=[50, 10], zoom_start=2)

geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"

cores_paises = {
    "Germany": "blue",
    "France": "blue",
    "United Kingdom": "blue",
    "Italy": "blue",
    "Austria": "blue",
    "Portugal": "yellow",
    "Brazil": "green"
}

folium.GeoJson(
    geojson_url,
    name="geojson",
    style_function=lambda x: {
        "fillColor": cores_paises.get(x["properties"]["ADMIN"], "white"),
        "color": "black",  # cor das bordas
        "fillOpacity": 0.4,  # opacidade do preenchimento
        "weight": 0.2,  # espessura do contorno
    },
).add_to(mapa)

st.title("Mapa dos países de origem")
folium_static(mapa)