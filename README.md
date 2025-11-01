# 🏦 Projeto de Análise de Câmbio: Ranking BACEN

Este projeto implementa uma solução robusta de Engenharia de Dados e Análise em Python para adquirir, unificar e tratar os dados históricos de Ranking de Câmbio do Banco Central do Brasil (BACEN), fornecendo uma base consolidada para análises futuras.

---

## 🛠️ Tecnologias e Bibliotecas

O projeto é construído em Python e utiliza uma arquitetura modular (`new_lib.py`) para isolar as lógicas de negócio.

| Módulo/Biblioteca | Foco Principal | Contribuição no Projeto |
| :--- | :--- | :--- |
| **`pandas`** | Análise e Engenharia de Dados | Unificação, limpeza, tratamento do DataFrame e resposta às 9 perguntas do case. |
| **`requests`** | Requisição Web | Download das bases ZIP do BACEN, testando dinamicamente múltiplos padrões de URL. |
| **`zipfile` / `io`** | Manipulação de Arquivos | Extração dos dados do ZIP em memória (`io.BytesIO`) e salvamento em disco. |
| **`chardet`** | Robustez de Leitura | Detecção automática do *encoding* de cada arquivo CSV, resolvendo problemas de acentuação. |
| **`openpyxl`** | Manipulação de Arquivos | Suporte para leitura de arquivos `.xlsx` (Exceções do BACEN). |
| **`plotly` / `plotly.express`** | Visualização Interativa | Geração dos gráficos dinâmicos (tendências, participação) exibidos no dashboard. |
| **`streamlit`** | Dashboard / Deployment | Framework para transformar o código Python em uma aplicação web interativa, hospedada na nuvem. |
| **`new_lib.py`** | Arquitetura | Módulo próprio que isola e organiza toda a lógica de negócio (download, unificar, tratar e analisar). |

---

## 📊 Estrutura do Projeto

O projeto é dividido em fases metodológicas de Aquisição, Tratamento e Análise.

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `main.py` | Script principal. Orquestra a execução das fases de aquisição, tratamento e, posteriormente, inicia a análise final. |
| `new_lib.py` | Biblioteca customizada contendo todas as funções de utilidade, download (`baixar_e_extrair_zip`), unificação (`unificar_bases`) e tratamento (`tratar_dados`). |
| `dados/` | **Pasta de Saída**. Armazena os arquivos baixados do BACEN (`zipfiles/`) e o resultado final do pipeline: `base_final_tratada_unica.csv`. |

---

## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:** O projeto requer as seguintes bibliotecas. Instale-as via terminal:
    ```bash
    pip install pandas requests openpyxl chardet
    ```

2.  **Configuração de Caminho:** O script `main.py` utiliza caminhos absolutos. **Altere a variável `DESTINO_BASE` no `main.py`** para o caminho local da sua máquina onde deseja armazenar os dados.

3.  **Execução:** Abra o terminal no diretório raiz do projeto e execute:
    ```bash
    python main.py
    ```

---

## ⚙️ Funcionalidades Automatizadas (Fase de Aquisição & Tratamento)

A implementação inclui soluções robustas de Engenharia de Dados para garantir a qualidade e completude da base histórica:

* **Automação Robusta de Download:** Utiliza laço de repetição (`for`) para cobrir o histórico de 2015 ao presente, testando **múltiplos padrões de URL** (`ESTATCAMBIF...`) para garantir a captura de todas as bases.
* **Gestão de Inconsistências:** Contempla uma rotina separada para a aquisição dos dados de 2014, cujas URLs não seguem o padrão regular do BACEN.
* **Unificação Inteligente:** Lê e concatena todos os arquivos (CSV e XLSX), utilizando:
    * Múltiplas tentativas de *header* (`header=4, 5, 6`) e *skiprows*.
    * Detecção de *encoding* (`chardet`) para resolver problemas de caracteres especiais.
* **Padronização e Limpeza:** O pipeline de tratamento (`tratar_dados`) realiza a padronização das colunas, remoção de linhas de metadados (`TOTAL GERAL`, `Fonte:`) e conversão para tipos numéricos.
* **Saída Final Consistente:** O arquivo final (`base_final_tratada_unica.csv`) é salvo com **encoding `utf-8-sig`**, garantindo a abertura correta de todos os caracteres em softwares como o Microsoft Excel.

---

## 🚀 Status e Próximos Passos

A fase de Engenharia de Dados (Aquisição e Tratamento) e a fase de Visualização estão concluídas. O projeto alcançou o objetivo de entregar uma base consolidada e um dashboard interativo.

| Fase | Status | Detalhes |
| :--- | :--- | :--- |
| **Aquisição & Tratamento** | **CONCLUÍDA** | Base `base_final_tratada_unica.csv` gerada, com saneamento e padronização histórica. |
| **Análise de Dados** | **CONCLUÍDA** | As 9 perguntas de negócio do CASE-EDUMI 2025 foram respondidas e integradas ao dashboard. |
| **Visualização (Dashboard)** | **CONCLUÍDA** | Aplicação web interativa desenvolvida com Plotly e Streamlit. |

---

## 🌐 Acesso ao Dashboard (Deployment)

O resultado da análise está acessível publicamente na nuvem, eliminando qualquer requisito de instalação local para visualização.

| Plataforma | URL de Acesso | Nota |
| :--- | :--- | :--- |
| **Streamlit Community Cloud** | **[Acessar o Dashboard de Câmbio](https://webscrappingbacen-jx9lqy3mmcyekfa5ihrzbf.streamlit.app)** | O servidor faz o *deploy* automático, lendo as dependências a partir do `requirements.txt`. |
---