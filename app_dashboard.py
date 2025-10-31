import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CAMINHO RELATIVO (ROBUSTO) ---
# O arquivo é esperado na subpasta 'dados' dentro da pasta de execução.
CAMINHO_DO_ARQUIVO = 'dados/base_final_tratada_unica.csv'


# --- Funções Auxiliares de Análise ---

def formatar_valor(valor):
    """Formata valor em USD com separador de milhar brasileiro."""
    # A verificação garante que a formatação só seja tentada em números válidos
    if pd.isna(valor):
        return None
    return f"US$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

def carregar_dados_e_analisar():
    """Carrega o DataFrame e prepara a análise, exibindo o dashboard."""
    st.set_page_config(layout="wide")
    st.title("🏦 Relatório Final de Análise de Câmbio (BACEN)")
    st.markdown("---")
    
    try:
        # Tenta carregar usando o caminho RELATIVO.
        df = pd.read_csv(CAMINHO_DO_ARQUIVO, sep=';', encoding='utf-8-sig')
    except FileNotFoundError:
        st.error("🚨 ERRO CRÍTICO: Arquivo não encontrado!")
        st.warning(f"O Streamlit não encontrou o arquivo no caminho relativo:")
        st.code(CAMINHO_DO_ARQUIVO)
        st.markdown("Verifique se você está executando o comando **`streamlit run app_dashboard.py`** na pasta **raiz** do projeto e se a pasta `dados` existe e não está vazia.")
        return

    if df.empty:
        st.warning("O DataFrame está vazio. Execute o main.py para preencher a base.")
        return

    # Preparação dos dados para análise
    df['Ano'] = df['Data_Ref'].str[:4]
    
    # ----------------------------------------------------
    # PERGUNTA 1: Valor total de operações de câmbio por ano
    # ----------------------------------------------------
    st.header("1. Valor total de operações de câmbio por ano")
    valor_por_ano = df.groupby('Ano')['Total_Geral_Valor'].sum().reset_index()
    
    # CORREÇÃO APLICADA: Aplicamos o apply diretamente na coluna Series e convertemos de volta para DataFrame
    df_formatado_p1 = valor_por_ano.set_index('Ano')['Total_Geral_Valor'].apply(formatar_valor).to_frame()
    
    # Gráfico Plotly
    fig1 = px.bar(
        valor_por_ano,
        x='Ano',
        y='Total_Geral_Valor',
        title='Evolução Anual do Valor Total de Câmbio',
        labels={'Total_Geral_Valor': 'Valor Total (US$)', 'Ano': 'Ano'},
        text=valor_por_ano['Total_Geral_Valor'].apply(lambda x: f"{x/1e9:.1f} B")
    )
    fig1.update_traces(marker_color='#007BFF')
    st.plotly_chart(fig1, use_container_width=True)
    st.dataframe(df_formatado_p1, use_container_width=True) # Usando DF formatado
    st.markdown("---")

    # ----------------------------------------------------
    # PERGUNTA 2: Top 5 Instituições com maior valor total de operações
    # ----------------------------------------------------
    st.header("2. Top 5 Instituições (Valor Total de Operações)")
    top_5_inst = df.groupby('Instituicao')['Total_Geral_Valor'].sum().nlargest(5).reset_index()
    
    # CORREÇÃO APLICADA
    df_formatado_p2 = top_5_inst.set_index('Instituicao')['Total_Geral_Valor'].apply(formatar_valor).to_frame()
    
    fig2 = px.pie(
        top_5_inst,
        values='Total_Geral_Valor',
        names='Instituicao',
        title='Participação do Top 5 no Valor Total de Câmbio'
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df_formatado_p2, use_container_width=True) # Usando DF formatado
    st.markdown("---")

    # ----------------------------------------------------
    # PERGUNTA 3: Valor total de Importação e Exportação por ano
    # ----------------------------------------------------
    st.header("3. Valor total de Importação e Exportação por ano")
    df_impexp = df.groupby('Ano')[['Importacao_Valor', 'Exportacao_Valor']].sum().reset_index()
    
    # CORREÇÃO APLICADA: Aplicamos apply com lambda para formatar múltiplas colunas (cell-wise)
    df_formatado_p3 = df_impexp.set_index('Ano').apply(lambda s: s.apply(formatar_valor))
    
    df_plot = df_impexp.melt(id_vars='Ano', value_vars=['Importacao_Valor', 'Exportacao_Valor'],
                             var_name='Tipo', value_name='Valor')
                             
    fig3 = px.line(
        df_plot,
        x='Ano',
        y='Valor',
        color='Tipo',
        title='Tendência Anual: Importação vs. Exportação (Valor)',
        markers=True
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(df_formatado_p3, use_container_width=True) # Usando DF formatado
    st.markdown("---")
    
    # ----------------------------------------------------
    # PERGUNTA 6: Valor total de Transferências
    # ----------------------------------------------------
    st.header("6. Valor total de Transferências (Entrada/Saída) por ano")
    df_transf = df.groupby('Ano')[['Transf_Exterior_Valor', 'Transf_pExterior_Valor']].sum().reset_index()

    # CORREÇÃO APLICADA
    df_formatado_p6 = df_transf.set_index('Ano').apply(lambda s: s.apply(formatar_valor))

    df_plot_transf = df_transf.melt(id_vars='Ano', value_vars=['Transf_Exterior_Valor', 'Transf_pExterior_Valor'],
                             var_name='Tipo', value_name='Valor')

    fig6 = px.bar(
        df_plot_transf,
        x='Ano',
        y='Valor',
        color='Tipo',
        title='Transferências Anuais (Entrada vs Saída)',
        barmode='group',
        labels={'Valor': 'Valor (US$)'}
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.dataframe(df_formatado_p6, use_container_width=True)
    st.markdown("---")


    # ----------------------------------------------------
    # PERGUNTAS DE TEXTO (Adaptadas)
    # ----------------------------------------------------
    
    st.header("Respostas Detalhadas")

    # 4. Qual a Instituição com maior valor de Exportação no último ano completo?
    ultimo_ano_base = df['Ano'].max()
    if df[df['Ano'] == ultimo_ano_base]['Data_Ref'].nunique() < 12:
         penultimo_ano = str(int(ultimo_ano_base) - 1)
    else:
         penultimo_ano = ultimo_ano_base
    df_penultimo = df[df['Ano'] == penultimo_ano]
    top_exp_penultimo = df_penultimo.groupby('Instituicao')['Exportacao_Valor'].sum().nlargest(1)
    st.markdown(f"**4. Instituição com maior Exportação em {penultimo_ano}:**")
    st.success(f"{top_exp_penultimo.index[0]} | Valor: {formatar_valor(top_exp_penultimo.iloc[0])}")

    # 5. Qual a Instituição com maior valor de Importação no ano de 2018?
    df_2018 = df[df['Ano'] == '2018']
    if not df_2018.empty:
        top_imp_2018 = df_2018.groupby('Instituicao')['Importacao_Valor'].sum().nlargest(1)
        st.markdown("**5. Instituição com maior Importação em 2018:**")
        st.success(f"{top_imp_2018.index[0]} | Valor: {formatar_valor(top_imp_2018.iloc[0])}")
    else:
        st.warning("5. Não há dados para 2018.")

    # 7. Qual o maior volume de Transações (Quantidade) de Exportação em 2020 (mês/instituição)?
    df_2020 = df[df['Ano'] == '2020']
    if not df_2020.empty:
        idx_max = df_2020['Exportacao_Quant'].idxmax()
        resultado = df_2020.loc[idx_max, ['Data_Ref', 'Instituicao', 'Exportacao_Quant']]
        quant_formatada = f"{resultado['Exportacao_Quant']:,.0f}".replace(',', '_').replace('.', ',').replace('_', '.')
        st.markdown("**7. Maior volume (Quantidade) de Exportação em 2020 (Mês/Instituição):**")
        st.info(f"Mês/Ano: {resultado['Data_Ref']} | Instituição: {resultado['Instituicao']} | Quantidade: {quant_formatada}")
    else:
        st.warning("7. Não há dados para 2020.")

    # 8. Qual a média de valor de operações de câmbio por instituição ao longo de todo o período?
    st.markdown("**8. Média de valor de operações de câmbio por instituição (Top 5):**")
    media_por_inst = df.groupby('Instituicao')['Total_Geral_Valor'].mean().sort_values(ascending=False)
    
    # CORREÇÃO APLICADA
    st.dataframe(media_por_inst.nlargest(5).apply(formatar_valor).to_frame(), use_container_width=True)
    st.markdown("...")


    # 9. Qual o total de operações (Valor) do Mercado Primário de Câmbio em todo o período?
    total_primario = df['Mercado_Primario_Valor'].sum()
    st.markdown("**9. Valor Total de Operações do Mercado Primário de Câmbio (Período Completo):**")
    st.success(f"Valor Total: {formatar_valor(total_primario)}")

# Chama a função principal
carregar_dados_e_analisar()