🏦 Projeto de Análise de Câmbio: Almeida LTDA & Banco Central do Brasil
Este projeto implementa uma solução de Engenharia de Dados e Análise em Python para atender aos requisitos da Almeida LTDA, conforme detalhado no CASE-EDUMI 2025.

O objetivo é automatizar a aquisição, unificação e tratamento dos dados de Ranking de Câmbio do Banco Central do Brasil (BACEN), fornecendo métricas para a tomada de decisão sobre operações cambiais.

🛠️ Tecnologias Utilizadas
Python: Linguagem principal para automação.
Pandas: Essencial para manipulação, unificação e análise dos dados.
Requests & Zipfile: Utilizados para a requisição HTTP e extração de arquivos ZIP diretamente do site do BACEN.
Módulos Próprios (new_lib.py): Arquitetura organizada em módulos (biblioteca própria) para garantir a reutilização e limpeza do código (requisito do Case).
📊 Estrutura do Projeto
O projeto é dividido em três fases metodológicas (Aquisição, Tratamento e Análise).

Arquivo/Pasta	Descrição
main.py	Script principal. Responsável por orquestrar a execução das fases, controlar o laço de repetição (for) e iniciar a análise final.
new_lib.py	Módulo (biblioteca própria) com funções utilitárias: criar_pasta, baixar_e_extrair_zip, unificar_bases, tratar_dados, etc.
dados/	Pasta de saída. Armazena os arquivos CSV baixados do BACEN (zipfiles/) e, futuramente, o base_consolidada_final.csv.
🚀 Como Executar o Projeto
Pré-requisitos: Certifique-se de ter o Python (com Spyder ou seu ambiente de preferência) e as bibliotecas pandas e requests instaladas.
Configuração de Caminho: O script main.py utiliza caminhos absolutos. Altere as variáveis DESTINO_BASE no main.py para o caminho local da sua máquina.
Execução: Execute o arquivo main.py.
⚙️ Funcionalidades Automatizadas
A implementação do projeto inclui:

Criação Estrutural de Pastas: Garante que a estrutura dados/ e dados/zipfiles/ exista.
Automação Híbrida de Download: Utiliza a lógica de laço de repetição (for) para baixar os dados de 2015 a 2025 (padrões [MM]-IF- e [MM]-[MM]) e trata a inconsistência do BACEN.
Unificação Inteligente: Lê todos os arquivos CSV extraídos, aplica correções essenciais e concatena-os em um único DataFrame.
Próximos passos após a aquisição: Finalizar o tratamento (nl.tratar_dados), iniciar a análise das 9 perguntas do case e desenvolver a crianção de dashboard.
