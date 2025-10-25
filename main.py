import sys
import os
import datetime
import importlib
import requests as r  
import pandas as pd
import new_lib as nl
import zipfile as z  # Apelido 'z' para zipfile
import io

sys.path.append(r'C:\Users\Isis\Documents\webscrapping_bacen') 
print(dir(nl)) 
print(nl.soma(2, 2))
print(nl)
print(pd)


DESTINO_BASE = r'C:\Users\Isis\Documents\webscrapping_bacen\dados'
nl.criar_pasta(DESTINO_BASE) 
DESTINO_ZIP_FILES = os.path.join(DESTINO_BASE, 'zipfiles')
nl.criar_pasta(DESTINO_ZIP_FILES) 
 

ANO_INICIAL = 2015
ANO_FINAL = datetime.date.today().year
print('\n--- INICIANDO FASE DE DOWNLOAD DAS BASES NO BACEN ---')

for ano in range(ANO_INICIAL, ANO_FINAL + 1):
    mes_limite = datetime.date.today().month if ano == ANO_FINAL else 12
    
    for mes in range(1, mes_limite + 1):
        info = nl.gerar_info_data(ano, mes)
        if info is None: continue
        
        url_download = info['url']
        
        if nl.baixar_e_extrair_zip(url_download, DESTINO_ZIP_FILES):
            print(f'Download e extração de {ano}-{mes} concluídos.')
        else:
            print(f'Arquivo não encontrado para {ano}-{mes}. Continuando processo de download.')
            

# BLOCO DE EXECUÇÃO MANUAL PARA 2014 (URL QUE NÃO SEGUE PADRÃO): 

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
    
    # Chamamos a função UMA ÚNICA VEZ e armazenamos o resultado (True ou False)
    download_sucesso = nl.baixar_e_extrair_zip(url_fixa, DESTINO_ZIP_FILES)
    
    # O if/else agora verifica o resultado e imprime a URL
    if download_sucesso:
        print(f'Download e extração de {url_fixa} concluídos.')
    else:
        print(f'Arquivo não encontrado para {url_fixa}. Continuando.')
        
print("--- Download de 2014 concluído. ---")
print("\n--- INICIANDO DIAGNÓSTICO ---")
nl.diagnostico_csv(DESTINO_ZIP_FILES) # <-- CHAMA A FUNÇÃO AQUI
print("--- FIM DO DIAGNÓSTICO ---")
# ... (código anterior do main.py) ...

print('---Fim da aquisição. Unificando todas as bases.')
df_consolidado = nl.unificar_bases(DESTINO_ZIP_FILES)
print(f"DEBUG: df_consolidado (type): {type(df_consolidado)}")

df_limpo = None # Garante que df_limpo exista no escopo, inicialmente como None

if df_consolidado is not None: 
    try:
        df_limpo = nl.tratar_dados(df_consolidado)
    except Exception as e:
        print(f"ERRO CRÍTICO no tratamento dos dados: {e}")
        # Se ocorrer um erro no tratamento, df_limpo permanece None e o código a seguir ignora o salvamento.

# Requisito 3.b: Salvar arquivo final em disco
if df_limpo is not None and len(df_limpo) > 0: # <-- VERIFICAÇÃO DUPLA AQUI!
    NOME_ARQUIVO_FINAL = os.path.join(DESTINO_BASE, 'base_final_tratada_unica.csv')
    
    # A linha que causava o erro agora só é executada se df_limpo for um DataFrame válido
    df_limpo.to_csv(NOME_ARQUIVO_FINAL, index=False, sep=';', encoding= 'latin1')

    print("\n========================================================")
    print(f"SUCESSO! PROJETO CONCLUÍDO.")
    print(f"A base tratada foi salva em: {NOME_ARQUIVO_FINAL}")
    print("========================================================")
else:
    print("\n========================================================")
    print("FALHA CRÍTICA! O DataFrame final (df_limpo) é nulo ou vazio. O arquivo não foi salvo.")
    print("Verifique as etapas de unificação (unificar_bases) ou tratamento (tratar_dados).")
    print("========================================================")