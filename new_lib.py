import re
import requests
import zipfile
import io
import os 
import datetime
import pandas as pd

def soma(a, b):
    """Retorna a soma de dois números."""
    return a + b

def criar_pasta(caminho):
    """Cria uma pasta se ela ainda não existir."""
    os.makedirs(caminho, exist_ok=True)
    print(f"Pasta criada/verificada: {caminho}")

def baixar_e_extrair_zip(url, destino_pasta):
    """Baixa o arquivo ZIP da URL e extrai o conteúdo para a pasta de destino."""
    print(f"Baixando ZIP de: {url}")
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(resposta.content)) as z:
            z.extractall(destino_pasta)
        print(f"Arquivos extraídos com sucesso em: {destino_pasta}")
        return True
    else:
        print(f"Erro ao baixar: Status Code {resposta.status_code}")
        return False
    

def gerar_info_data(ano, mes):
    try:
        data = datetime.date(ano, mes, 1)
    except ValueError:
        return None # Data inválida

    mes_num_2d = data.strftime("%m") # Ex: '01', '09'
    ano_str = str(ano)
    
    # Padrão identificado: Letra fixa (f) + ANO + MÊS 
    prefixo = f'ESTATCAMBIF{ano_str}{mes_num_2d}'
    
    #1. PADRÃO 1 (2025): SEM O -IF-
    if ano == 2025:
        sufixo = f'-{ano_str}{mes_num_2d}.zip'
        
    #2. PADRÃO 2 (2015-2024): COM O -IF-
    elif ano >= 2015 and ano <= 2024:
        sufixo = f'-IF-{ano_str}{mes_num_2d}.zip'
        
    #3. EXCEÇÃO: Anos fora do padrão (2014)
    else: 
        #Não há lógica aplicada aqui.
        return None
    
    url_padrao = prefixo + sufixo 
    
    return{
        'url': f"https://www.bcb.gov.br/content/estatisticas/rankingcambioinstituicoes/{url_padrao}",
        'filename_csv': f"Ranking Instituição {ano_str} {mes_num_2d}.csv"
        }
    

# UNIFICAR BASES
# ARQUIVO: new_lib.py (Função unificar_bases - Foco na Indentação)

def unificar_bases(pasta_csv):
    lista_dfs = []
    arquivos = os.listdir(pasta_csv)
    
    print(f'Iniciando unificação de {len(arquivos)} arquivos na pasta...')
    
    for nome_arquivo in arquivos: 
        if nome_arquivo.endswith('.csv') and not nome_arquivo.startswith('~'):
            caminho_completo = os.path.join(pasta_csv, nome_arquivo)
            df = None
            
            # TENTATIVA 1: CSV com HEADER 4 (índice 4)
            try:
                df = pd.read_csv(caminho_completo, sep=';', encoding='latin1', header=4, thousands='.')
            except Exception:
                pass

            # TENTATIVA 2: CSV com HEADER 5 (índice 5)
            if df is None: 
                try:
                    df = pd.read_csv(caminho_completo, sep=';', encoding='latin1', header=5, thousands='.')
                except Exception: 
                    pass
                    
            # TENTATIVA 3: EXCEL (XLS/XLSX disfarçado)
            if df is None: 
                try: 
                    df = pd.read_excel(caminho_completo, header=4)
                except Exception as e: 
                    print(f'⚠️ Falha: Não foi possível ler {nome_arquivo}. Pulando arquivo.')
                    continue # 🛑 Se tudo falhar, PULA O ARQUIVO. 
                    
            # BLOCO DE PROCESSAMENTO (EXECUTA SOMENTE SE A LEITURA FOI UM SUCESSO)
            if df is not None: 
                partes_nome = nome_arquivo.split(' ')
                if len(partes_nome) >= 4:
                    ano = partes_nome[2]
                    mes = partes_nome[3].split('.')[0]
                    df['Data_Ref'] = f'{ano}-{mes}'
                        
                lista_dfs.append(df)
                print(f'-> {nome_arquivo} carregado ({len(df)} linhas).')
                
    # 🛑 ESTE É O BLOCO CRÍTICO: DEVE ESTAR FORA DO FOR LOOP, NO NÍVEL DA FUNÇÃO
    # Remova todo o recuo anterior, garantindo que ele esteja no mesmo nível do 'for nome_arquivo in arquivos:'
    if not lista_dfs: 
        print(f'❌ Nenhum DataFrame CSV válido encontrado para unificar.')
        return None
    
    df_consolidado = pd.concat(lista_dfs, ignore_index = True)
    print(f'✅ Bases unificadas com sucesso! Total de linhas: {len(df_consolidado)}.')
    
    return df_consolidado # 🛑 ESTE É O RETURN QUE ESTAVA DANDO ERRO!
    
    # ETAPA DE TRATAMENTO DE DADOS: 

def tratar_dados(df): 
    
    # 0. Checagem inicial de DF vazio
    if df is None or len(df) == 0:
        print("🛑 ERRO: DataFrame consolidado recebido é nulo ou vazio.")
        return None

    # 1. REMOÇÃO DE LINHAS DE SUJEIRA E METADADOS
    
    # 🛑 ATUALIZAÇÃO 1: Remoção de Linhas de Metadados (TOTAL, Fonte, Obs.)
    filtro_remover = [
        'TOTAL GERAL', 
        'Fonte:', 
        'Obs.',
        'TOTAL DE' # Adicionado um filtro genérico de Total
    ]
    
    # Constrói o filtro de string
    filtro_completo = '|'.join(filtro_remover)
    
    # 🛑 Assegura que a primeira coluna é string antes de filtrar
    df.iloc[:, 0] = df.iloc[:, 0].astype(str)
    
    # Filtra: Remove todas as linhas que contenham as palavras de filtro na primeira coluna
    df = df[~df.iloc[:, 0].str.contains(filtro_completo, case=False, na=False)]
    
    # 🛑 ATUALIZAÇÃO 2: Remove linhas que estão inteiramente vazias (NaN) na coluna Instituicao
    df = df.dropna(subset=['Instituicao'])
    
    print("✅ Linhas de 'TOTAL GERAL' e metadados removidas.")
    
    # 2. Checagem de DF vazio após filtros
    if len(df) == 0:
        print("🛑 ERRO: DataFrame ficou vazio após remover sujeira.")
        return None

    # 3. RENOMEAR COLUNAS (Ajustado para 23 colunas, conforme seu debug)
    novos_nomes = [ 
        'Rank', 'Codigo_Instituicao', 'Instituicao', 
        'Exportacao_Quant', 'Exportacao_Valor', 'Importacao_Quant', 'Importacao_Valor', 
        'Transf_Exterior_Quant', 'Transf_Exterior_Valor', 'Transf_pExterior_Quant', 'Transf_pExterior_Valor', 
        'Mercado_Primario_Quant', 'Mercado_Primario_Valor',
        'Interbancario_C_Quant', 'Interbancario_C_Valor', 'Interbancario_V_Quant', 'Interbancario_V_Valor',
        'Mercado_Interbancario_Quant', 'Mercado_Interbancario_Valor', 'Total_Geral_Quant', 'Total_Geral_Valor', 
        'Extra_Vazia_1', 'Data_Ref' # Lista final de 23 nomes
    ]

    num_cols_atual = len(df.columns)
    print(f"DEBUG: Tratamento - Colunas recebidas: {num_cols_atual}")
    
    # Renomeação: Usa a lista de novos nomes, truncando a lista para o tamanho real do DF
    df.columns = novos_nomes[:num_cols_atual]
    print("✅ Colunas renomeadas.")
    
    # 4. FILTRAR DADOS INTERBANCÁRIOS (Remoção de Colunas)
    cols_interbancarias = ['Interbancario_C_Valor', 'Interbancario_V_Valor', 
                           'Interbancario_C_Quant', 'Interbancario_V_Quant']
                           
    cols_to_drop = [col for col in cols_interbancarias if col in df.columns]

    df_final = df.drop(columns=cols_to_drop)
    print("✅ Colunas interbancárias removidas.")
    
    # 5. GARANTIR TIPOS NUMÉRICOS (Limpeza e Conversão)
    cols_valor_quant = [col for col in df_final.columns if 'Valor' in col or 'Quant' in col]
    
    for col in cols_valor_quant:
        # 🛑 Adição de pré-limpeza robusta para garantir que apenas números sejam passados
        if df_final[col].dtype == 'object':
            df_final[col] = (df_final[col]
                             .astype(str) 
                             .str.replace(r'[^\d\.\,]', '', regex=True) # Remove R$, espaços, etc.
                             .str.replace('.', '', regex=False)        # Remove separadores de milhar
                             .str.replace(',', '.', regex=False)        # Troca vírgula decimal por ponto
                             .str.strip()
                            )
            
        # Converte para numérico (errors='coerce' transforma falhas de conversão em NaN)
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce') 
        
    print("✅ Tipos de dados de valor e quantidade convertidos para numérico.")
    
    return df_final

    # 3. FILTRAR DADOS INTERBANCÁRIOS (Requisito Gobberman)
    cols_interbancarias = ['Interbancario_C_Valor', 'Interbancario_V_Valor', 
                           'Interbancario_C_Quant', 'Interbancario_V_Quant']
                           
    cols_to_drop = [col for col in cols_interbancarias if col in df.columns]

    df_final = df.drop(columns=cols_to_drop, errors='ignore') # Adicionado errors='ignore' para robustez
    print("✅ Colunas interbancárias removidas.")
    
    # 4. GARANTIR TIPOS NUMÉRICOS (Requisito 2.b.i)
    # 4. GARANTIR TIPOS NUMÉRICOS (Requisito 2.b.i)
cols_valor_quant = [col for col in df_final.columns if 'Valor' in col or 'Quant' in col]

for col in cols_valor_quant:
    # 🛑 SOLUÇÃO ROBUSTA: USAR REGEX PARA REMOVER TUDO, EXCETO DÍGITOS E PONTOS
    if df_final[col].dtype == 'object':
        df_final[col] = (df_final[col]
                         .astype(str) 
                         # Remove *qualquer* caractere que não seja dígito, vírgula ou ponto.
                         .str.replace(r'[^\d\.\,]', '', regex=True) # <- REMOVE R$, ESPAÇOS, etc.
                         .str.replace('.', '', regex=False) # Remove separadores de milhar (ponto)
                         .str.replace(',', '.', regex=False) # Troca vírgula decimal por ponto
                         .str.strip()
                        )
        
    df_final[col] = pd.to_numeric(df_final[col], errors='coerce')

    print("✅ Tipos de dados de valor e quantidade convertidos para numérico.")
    
    # 3. Checagem final: se o DF está vazio após o tratamento
    if len(df_final) == 0:
        print("🛑 ERRO: DataFrame final está vazio. Retornando None.")
        return None
        
    return df_final
        
