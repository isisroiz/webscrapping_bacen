import re
import requests
import zipfile
import io
import os
import datetime
import pandas as pd
import unicodedata 
import shutil 
import chardet 

# =======================================================
# UTILS GERAIS
# =======================================================

def soma(a, b):
    """Retorna a soma de dois números."""
    return a + b

def criar_pasta(caminho):
    """Cria uma pasta se ela ainda não existir."""
    os.makedirs(caminho, exist_ok=True)
    print(f"Pasta criada/verificada: {caminho}")

def renomear_arquivos_extraidos(dest_dir, ano, mes):
    """
    Renomeia arquivos extraídos do ZIP para um padrão limpo:
    ranking_AAAA-MM_mensal.csv ou ranking_AAAA-MM_acumulado.csv
    """
    for nome_original in os.listdir(dest_dir):
        caminho_antigo = os.path.join(dest_dir, nome_original)
        nome_limpo = unicodedata.normalize('NFKD', nome_original).encode('ascii', 'ignore').decode('ascii').lower()

        if not os.path.isfile(caminho_antigo):
            continue

        ext = os.path.splitext(nome_original)[1].lower()
        novo_nome = None
        mes_str = str(mes).zfill(2)
        ano_str = str(ano)

        if "acumulado" in nome_limpo:
            novo_nome = f"ranking_{ano_str}-{mes_str}_acumulado{ext}"

        elif ext == '.csv' and "mensal" not in nome_limpo and "acumulado" not in nome_limpo:
            novo_nome = f"ranking_{ano_str}-{mes_str}_mensal{ext}"

        elif ext in ['.xlsx', '.xls']:
            novo_nome = f"ranking_{ano_str}-{mes_str}{ext}"

        if novo_nome:
            caminho_novo = os.path.join(dest_dir, novo_nome)
            try:
                os.rename(caminho_antigo, caminho_novo)
                print(f"✅ Renomeado: {nome_original} -> {novo_nome}")
            except Exception as e:
                print(f"❌ Erro ao renomear {nome_original}: {e}")
        else:
            print(f"⚠️ Ignorado: {nome_original}")
            
def detectar_encoding(caminho, amostra=40000):
    """Detecta o encoding do arquivo."""
    try:
        with open(caminho, 'rb') as f:
            return chardet.detect(f.read(amostra)).get('encoding', 'latin1')
    except Exception:
        return 'latin1'

# =======================================================
# DOWNLOAD E GERAÇÃO DE URL
# =======================================================

def baixar_e_extrair_zip(url, destino_pasta, ano, mes):
    """Baixa o arquivo ZIP, extrai para pasta temp, renomeia e move."""
    mes_str = str(mes).zfill(2)
    ano_str = str(ano)

    print(f"Baixando ZIP de: {url}")
    resposta = requests.get(url)

    if resposta.status_code == 200:
        temp_dir = os.path.join(destino_pasta, f"temp_{ano_str}_{mes_str}")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(io.BytesIO(resposta.content)) as z:
                z.extractall(temp_dir)
            
            renomear_arquivos_extraidos(temp_dir, ano, mes)

            for arquivo in os.listdir(temp_dir):
                origem = os.path.join(temp_dir, arquivo)
                destino = os.path.join(destino_pasta, arquivo)
                if not os.path.exists(destino):
                    shutil.move(origem, destino)
                else:
                    print(f"⚠️ Já existe no destino: {arquivo}, ignorando movimento.")
            
            shutil.rmtree(temp_dir)

            print(f"Arquivos extraídos e renomeados com sucesso em: {destino_pasta}")
            return True
        
        except zipfile.BadZipFile:
            print('❌ Erro: arquivo não é um ZIP válido.')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return False
        
        except Exception as e:
            print(f"❌ Erro na extração ou renomeação: {e}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return False

    else:
        return False
    
def gerar_info_data(ano, mes):
    """Gera e testa múltiplos padrões de URL do BACEN."""
    try:
        data = datetime.date(ano, mes, 1)
    except ValueError:
        return None

    mes_num_2d = data.strftime("%m")
    ano_str = str(ano)

    padroes = [
        f'ESTATCAMBIF{ano_str}{mes_num_2d}-IF-{ano_str}{mes_num_2d}.zip',
        f'ESTATCAMBIF{ano_str}{mes_num_2d}-{ano_str}{mes_num_2d}.zip',
        f'ESTATCAMBIF{ano_str}{mes_num_2d}-IF_{ano_str}{mes_num_2d}.zip',
        f'ESTATCAMBIF{ano_str}{mes_num_2d}-AT_{ano_str}-{mes_num_2d}.zip',
        f'ESTATCAMBIF{ano_str}{mes_num_2d}-IF-{ano_str}-{mes_num_2d}.zip',
        f'ESTATCAMBIF{ano_str}{mes_num_2d}IF-{ano_str}{mes_num_2d}.zip',
        f'ESTATCAMBIF{ano_str}{mes_num_2d}-Ranking%20Institui%C3%A7%C3%A3o%20{ano_str}%20{mes_num_2d}.xls',
        f'ESTATCABIF{ano_str}{mes_num_2d}IF-{ano_str}{mes_num_2d}.zip',
    ]
    
    BASE_URL = "https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/"

    for padrao in padroes:
        url = BASE_URL + padrao
        try:
            r = requests.head(url, timeout=5)
            if r.status_code == 200:
                print(f'URL encontrada (Padrão: {padrao})')
                return url
        except requests.RequestException:
            continue
            
    return None

# =======================================================
# UNIFICAR BASES
# =======================================================

COLUNAS_PADRAO = [
    "Rank", "Codigo_Instituicao", "Instituicao",
    "Exportacao_Quant", "Exportacao_Valor", 
    "Importacao_Quant", "Importacao_Valor",
    "Transf_Exterior_Quant", "Transf_Exterior_Valor", 
    "Transf_pExterior_Quant", "Transf_pExterior_Valor",
    "Mercado_Primario_Quant", "Mercado_Primario_Valor",
    "Interbancario_C_Quant", "Interbancario_C_Valor", 
    "Interbancario_V_Quant", "Interbancario_V_Valor",
    "Mercado_Interbancario_Quant", "Mercado_Interbancario_Valor", 
    "Total_Geral_Quant", "Total_Geral_Valor",
]

def unificar_bases(pasta_csv):
    lista_dfs = []
    padrao_limpo = re.compile(r'^ranking_(\d{4})-(\d{2})_mensal\.csv$', flags=re.IGNORECASE)
    arquivos = sorted([f for f in os.listdir(pasta_csv) if padrao_limpo.match(f)])

    if not arquivos:
        arquivos = sorted([f for f in os.listdir(pasta_csv) if f.endswith('.csv') and not f.startswith('~')])
        if not arquivos:
            print(f'❌ Nenhum DataFrame CSV encontrado para unificar.')
            return None
        print(f'✅ Usando fallback: Encontrados {len(arquivos)} arquivos CSV com nomes não padronizados.')


    print(f'Iniciando unificação de {len(arquivos)} arquivos na pasta...')

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(pasta_csv, nome_arquivo)
        df = None
        
        match_padrao = padrao_limpo.match(nome_arquivo)
        if match_padrao:
            ano_str, mes_str = match_padrao.groups()
        else:
            partes_nome = nome_arquivo.split(' ')
            if len(partes_nome) >= 4:
                ano_str = partes_nome[2]
                mes_str = partes_nome[3].split('.')[0].zfill(2)
            else:
                ano_str, mes_str = '9999', '99'

        enc = detectar_encoding(caminho_completo)

        headers = [4, 5, 6]
        for header_idx in headers:
            try:
                df = pd.read_csv(caminho_completo, sep=';', encoding=enc, header=header_idx, thousands='.', skipinitialspace=True)
                if df.shape[1] >= 10 and len(df) > 0:
                    break
                df = None
            except Exception:
                pass

        if df is None:
             try: 
                 df = pd.read_csv(
                     caminho_completo,
                     sep=';',
                     skiprows=7,
                     header=None,
                     encoding=enc,
                     engine='python'
                 )
             except Exception:
                 pass

        if df is None or len(df) == 0:
            try:
                df = pd.read_excel(caminho_completo, header=4, skipfooter=1, engine='openpyxl')
            except Exception:
                print(f'⚠️ Falha: Não foi possível ler {nome_arquivo}. Pulando arquivo.')
                continue

        if df is not None and len(df) > 0:
            
            num_cols_df = df.shape[1]
            if num_cols_df < len(COLUNAS_PADRAO):
                 faltantes = len(COLUNAS_PADRAO) - num_cols_df
                 for i in range(faltantes):
                     df[f'Extra_Vazia_{i+1}'] = None
            elif num_cols_df > len(COLUNAS_PADRAO):
                 df = df.iloc[:, :len(COLUNAS_PADRAO)]
            
            df.columns = COLUNAS_PADRAO 

            df['Data_Ref'] = f'{ano_str}-{mes_str}'
            
            lista_dfs.append(df)
            print(f'-> {nome_arquivo} carregado ({len(df)} linhas).')

    if not lista_dfs:
        print(f'❌ Nenhum DataFrame válido encontrado para unificar.')
        return None

    df_consolidado = pd.concat(lista_dfs, ignore_index=True)
    print(f'✅ Bases unificadas com sucesso! Total de linhas: {len(df_consolidado)}.')

    return df_consolidado

# =======================================================
# TRATAMENTO DE DADOS
# =======================================================
def tratar_dados(df):
    
    if df is None or len(df) == 0:
        print("🛑 ERRO: DataFrame consolidado recebido é nulo ou vazio.")
        return None

    filtro_remover = [
        'TOTAL GERAL',
        'Fonte:',
        'Obs.',
        'TOTAL DE',
        'Valor (US$)'
    ]
    
    filtro_completo = '|'.join(filtro_remover)
    
    df = df[~df['Instituicao'].astype(str).str.contains(filtro_completo, case=False, na=False)]
    
    df = df.dropna(subset=['Instituicao', 'Exportacao_Valor'])
    
    print("✅ Linhas de 'TOTAL GERAL' e metadados removidas.")
    
    if len(df) == 0:
        print("🛑 ERRO: DataFrame ficou vazio após remover sujeira.")
        return None

    novos_nomes = [
        'Rank', 'Codigo_Instituicao', 'Instituicao',
        'Exportacao_Quant', 'Exportacao_Valor', 'Importacao_Quant', 'Importacao_Valor',
        'Transf_Exterior_Quant', 'Transf_Exterior_Valor', 'Transf_pExterior_Quant', 'Transf_pExterior_Valor',
        'Mercado_Primario_Quant', 'Mercado_Primario_Valor',
        'Interbancario_C_Quant', 'Interbancario_C_Valor', 'Interbancario_V_Quant', 'Interbancario_V_Valor',
        'Mercado_Interbancario_Quant', 'Mercado_Interbancario_Valor', 'Total_Geral_Quant', 'Total_Geral_Valor',
    ]
    
    num_cols_atual = len(df.columns)
    
    nomes_reais = novos_nomes
    if 'Data_Ref' in df.columns:
         nomes_reais.append('Data_Ref')
    
    colunas_extras_no_df = [col for col in df.columns if col.startswith('Extra_Vazia_')]
    for col_extra in colunas_extras_no_df:
        nomes_reais.append(col_extra)

    df.columns = nomes_reais[:num_cols_atual]
    
    print("✅ Colunas renomeadas.")
    
    cols_interbancarias = ['Interbancario_C_Valor', 'Interbancario_V_Valor',
                           'Interbancario_C_Quant', 'Interbancario_V_Quant']
                           
    cols_to_drop = [col for col in cols_interbancarias if col in df.columns]

    df_final = df.drop(columns=cols_to_drop, errors='ignore')
    print("✅ Colunas interbancárias removidas.")
    
    cols_valor_quant = [col for col in df_final.columns if 'Valor' in col or 'Quant' in col]

    for col in cols_valor_quant:
        if df_final[col].dtype == 'object':
            df_final[col] = (df_final[col]
                             .astype(str)
                             .str.replace(r'[^\d\.\,\-]', '', regex=True)
                             .str.replace('.', '', regex=False)
                             .str.replace(',', '.', regex=False)
                             .str.strip()
                            )

        df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
        
    print("✅ Tipos de dados de valor e quantidade convertidos para numérico.")
    
    if len(df_final) == 0:
        print("🛑 ERRO: DataFrame final está vazio. Retornando None.")
        return None
        
    return df_final