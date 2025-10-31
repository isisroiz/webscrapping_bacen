# 🏦 Projeto de Análise de Câmbio: Ranking BACEN

Este projeto implementa uma solução robusta de Engenharia de Dados e Análise em Python para adquirir, unificar e tratar os dados históricos de Ranking de Câmbio do Banco Central do Brasil (BACEN), fornecendo uma base consolidada para análises futuras.

---

## 🛠️ Tecnologias e Bibliotecas

O projeto é construído em Python e utiliza uma arquitetura modular (`new_lib.py`) para isolar as lógicas de negócio.

| Módulo/Biblioteca | Foco Principal | Contribuição no Projeto |
| :--- | :--- | :--- |
| **`pandas`** | Análise e Engenharia de Dados | Unificação de todos os CSVs/XLSX mensais em um único DataFrame, limpeza, tipagem e filtragem de colunas. |
| **`requests`** | Requisição Web | Download das bases ZIP do BACEN, testando dinamicamente múltiplos padrões de URL. |
| **`zipfile` / `io`** | Manipulação de Arquivos | Extração dos dados do ZIP em memória (`io.BytesIO`) e salvamento em disco. |
| **`chardet`** | Robustez de Leitura | Detecção automática do *encoding* de cada arquivo CSV, resolvendo problemas de acentuação (UTF-8, Latin1, etc.) durante a unificação. |
| **`openpyxl`** | Manipulação de Arquivos | Suporte para leitura de arquivos `.xlsx` que o BACEN ocasionalmente disponibiliza, garantindo a ingestão completa. |
| **`new_lib.py`** | Arquitetura | Módulo próprio que isola e organiza toda a lógica de negócio (download, unificar e tratar), promovendo a modularidade do código. |

---

## 📊 Estrutura do Projeto

O projeto é dividido em fases metodológicas de Aquisição, Tratamento e Análise.

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `main.py` | Script principal. Orquestra a execução das fases de aquisição, tratamento e, posteriormente, inicia a análise final. |
| `new_lib.py` | Biblioteca customizada contendo todas as funções de utilidade, download (`baixar_e_extrair_zip`), unificação (`unificar_bases`) e tratamento (`tratar_dados`). |
|

