# 🏦 Projeto de Análise de Câmbio: Almeida LTDA & Banco Central do Brasil

Este projeto implementa uma solução de Engenharia de Dados e Análise em Python para atender aos requisitos da Almeida LTDA, conforme detalhado no CASE-EDUMI 2025.
O objetivo é automatizar a aquisição, unificação e tratamento dos dados de Ranking de Câmbio do Banco Central do Brasil (BACEN), fornecendo métricas para a tomada de decisão sobre operações cambiais.

---

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal para automação.
* **Pandas:** Essencial para manipulação, unificação e análise dos dados.
* **Requests & Zipfile:** Utilizados para a requisição HTTP e extração de arquivos ZIP diretamente do site do BACEN.
* **chardet & unicodedata:** Bibliotecas adicionais para garantir a leitura correta de diferentes *encodings* de arquivo e padronização de nomes.
* **Módulos Próprios (new_lib.py):** Arquitetura organizada em módulos (biblioteca própria) para garantir a reutilização e limpeza do código (requisito do Case).

---

## 📊 Estrutura do Projeto

O projeto é dividido em três fases metodológicas (Aquisição, Tratamento e Análise).

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `main.py` | Script principal. Responsável por orquestrar a execução das fases, controlar o laço de repetição (`for`) e iniciar a análise final. |
| `new_lib.py` | Módulo (biblioteca própria) com funções utilitárias: `criar_pasta`, `baixar_e_extrair_zip`, `unificar_bases`, `tratar_dados`, etc. |
| `dados/` | Pasta de saída. Armazena os arquivos CSV baixados do BACEN (`zipfiles/`) e o resultado final em `base_final_tratada_unica.csv`. |

---

## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:** Certifique-se de ter o Python instalado e as bibliotecas essenciais: `pandas`, `requests`, `openpyxl`, **`chardet`** e `unidecode`. Instale-as via terminal:
    ```bash
    pip install pandas requests openpyxl chardet
    ```
2.  **Configuração de Caminho:** O script `main.py` utiliza caminhos absolutos. Altere as variáveis `DESTINO_BASE` no `main.py` para o caminho local da sua máquina.
3.  **Execução:** Abra o terminal no diretório do projeto e execute:
    ```bash
    python main.py
    ```

---

## ⚙️ Funcionalidades Automatizadas

A implementação do projeto inclui soluções de Engenharia de Dados para garantir a qualidade da base:

* **Criação Estrutural de Pastas:** Garante que a estrutura `dados/` e `dados/zipfiles/` exista.
* **Automação Híbrida de Download:** Utiliza a lógica de laço de repetição (`for`) para baixar os dados de 2015 ao presente, testando **múltiplos padrões de URL** do BACEN.
* **Tratamento de Exceção (2014):** Contempla uma rotina separada para a aquisição dos dados de 2014, cujas URLs não seguem um padrão regular.
* **Unificação Inteligente:** Lê **todos** os arquivos CSV extraídos (e `.xlsx` em caso de exceção), aplicando detecção de *encoding* (`chardet`) para garantir a correta leitura dos caracteres especiais (acentos, símbolos).
* **Padronização de Saída:** O arquivo final (`base_final_tratada_unica.csv`) é salvo no formato CSV, com separador `;` e **encoding `utf-8-sig`** para evitar erros de caracteres e garantir a compatibilidade com o Excel.

---

## Próximos Passos

Após a aquisição e tratamento (fase concluída), o foco é:

1.  Desenvolver a análise de dados para responder às 9 perguntas do case.
2.  Desenvolver a criação do dashboard de visualização.
