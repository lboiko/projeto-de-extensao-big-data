import streamlit as st
import pandas as pd
import plotly.express as px


# Ler o arquivo Excel (substitua 'arquivo.xlsx' pelo caminho do seu arquivo)
df = pd.read_excel('dados/porsche_dados.xlsx')

# Converter e salvar como CSV (substitua 'saida.csv' pelo nome desejado para o arquivo CSV)
# df.to_csv('porsche_data.csv', index=False)

print(df.columns)
# df.rename(columns={
#     'id linha': 'ID',
#     'CAT.': 'Categoria',
#     'PROCESSO': 'Processo',
#     'QNT': 'Quantidade',
#     'DESCRIPTION': 'Descrição',
#     'BRAND': 'Marca',
#     'SERIAL No.': "Número de série",
#     'MADE IN': 'Fabricação',
#     'UNIT VALUE': 'Valor da unidade',
#     'TOTAL VALUE': 'Valor total',
#     'UNIT NET WEIGHT': 'Peso da unidade',
#     'TOTAL NET WEIGHT': 'Pessoal por tipo de peça',
#     'NAC / PORT / MIA': 'Porto de saída'
# }, inplace=True)

st.title("Visualização de Dados")

#Barra Lateral para opções de filtragem
st.sidebar.header("Opções de Filtro")

pais_selecionado = st.sidebar.selectbox(
    "Selecione o Local",
    options=df['MADE IN'].unique(),
    index=0
)


#Aplicar filtros ao dataset

dados_filtrados = df[(df['MADE IN'] == pais_selecionado)]
                       

#Exibir dados filtrados
st.write(f'### Dados filtrados para {pais_selecionado}', dados_filtrados)

#Visualização 1: Quantidade por País
quantidade_por_categoria = dados_filtrados.groupby('BRAND')['QNT'].sum().reset_index()
fig_quantidade = px.bar(quantidade_por_categoria, x='Marca', y='Quantidade',
                        title=f'Quantidade Total por Marca - {pais_selecionado}')
st.plotly_chart(fig_quantidade)

