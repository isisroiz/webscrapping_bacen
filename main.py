import sys
import os
import datetime
import importlib
import requests as r
import pandas as pd
import new_lib as nl
import zipfile as z 
import io
import shutil 

sys.path.append(r'C:\Users\Isis\Documents\webscrapping_bacen')
print(dir(nl))
print(nl.soma(2, 2))
print(nl)
print(pd)


DESTINO_BASE = r'C:\Users\Isis\Documents\webscrapping_bacen\dados' # ALVO DE CONFIGURAÇÃO!
nl.criar_pasta(DESTINO_BASE)
DESTINO_ZIP_FILES = os.path.join(DESTINO_BASE, 'zipfiles')
nl.criar_pasta(DESTINO_ZIP_FILES)


ANO_INICIAL = 2015
ANO_FINAL = datetime.date.today().year
print('\n--- INICIANDO FASE DE DOWNLOAD DAS BASES NO BACEN ---')

for ano in range(ANO_INICIAL, ANO_FINAL + 1):
    mes_limite = datetime.date.today().month if ano == ANO_FINAL else 12

    for mes in range(1, mes_limite + 1):
        url_download = nl.gerar_info_data(ano, mes)
        if url_download is None: continue

        if nl.baixar_e_extrair_zip(url_download, DESTINO_ZIP_FILES, ano, mes):
            print(f'Download e extração de {ano}-{mes} concluídos.')
        else:
            print(f'Arquivo não encontrado para {ano}-{mes}. Continuando processo de download.')


# BLOCO DE EXECUÇÃO MANUAL PARA 2014 (URLS QUE NÃO SEGUEM PADRÃO):

URLS_MANUAIS_2014 = [
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201412-IF-201412.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201410-AT_2014-10.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201409-IF-201409.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201408-IF-201408.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201407-IF-201407.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201406-IF-201406.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201405-IF-201405.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201404-IF-201404.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201403-IF-201403.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201402-IF-201402.zip',
    r'https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/ESTATCAMBIF201401-IF_201401.zip',
         ]

print("\n--- INICIANDO DOWNLOAD MANUAL PARA 2014 ---")
for url_fixa in URLS_MANUAIS_2014:
    if nl.baixar_e_extrair_zip(url_fixa, DESTINO_ZIP_FILES, 2014, 0):
        print(f'Download e extração de {url_fixa} concluídos.')
    else:
        print(f'Arquivo não encontrado para {url_fixa}. Continuando.')

print("--- Download de 2014 concluído. ---")

print('---Fim da aquisição. Unificando todas as bases.')
df_consolidado = nl.unificar_bases(DESTINO_ZIP_FILES)
print(f"DEBUG: df_consolidado (type): {type(df_consolidado)}")

df_limpo = None 

if df_consolidado is not None:
    try:
        df_limpo = nl.tratar_dados(df_consolidado)
        
        # CHAMA A FASE DE ANÁLISE!
        if df_limpo is not None:
            nl.analisar_dados(df_limpo)

    except Exception as e:
        print(f"ERRO CRÍTICO no tratamento dos dados: {e}")

# Requisito 3.b: Salvar arquivo final em disco
if df_limpo is not None and len(df_limpo) > 0:
    NOME_ARQUIVO_FINAL = os.path.join(DESTINO_BASE, 'base_final_tratada_unica.csv')

    # Correção do Encoding
    df_limpo.to_csv(NOME_ARQUIVO_FINAL, index=False, sep=';', encoding= 'utf-8-sig')

    print("\n========================================================")
    print(f"SUCESSO! PROJETO CONCLUÍDO.")
    print(f"A base tratada foi salva em: {NOME_ARQUIVO_FINAL}")
    print("========================================================")
else:
    print("\n========================================================")
    print("FALHA CRÍTICA! O DataFrame final (df_limpo) é nulo ou vazio. O arquivo não foi salvo.")
    print("Verifique as etapas de unificação (unificar_bases) ou tratamento (tratar_dados).")
    print("========================================================")