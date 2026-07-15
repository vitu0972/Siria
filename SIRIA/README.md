# SIRIA

Siria é uma ferramenta de avaliação de riscos com relatório gerado por IA, junto a uma linguagem adaptada para o setor alvo da avaliação. Tem como público alvo profissionais de Segurança em TI.

# Funcionalidades

- Cadastro de riscos com cálculo automático (Impacto × Probabilidade)
- Classificação por matriz de risco (ISO 27005)
- Tabela de resultados com codificação de cores por severidade
- Geração de relatórios com linguagem adaptada por setor via IA (Groq / LLaMA 3)
- Suporte a ingestão de políticas de segurança em PDF como contexto para a IA

# Ferramentas usadas

- Python 3.12
- Tkinter (interface gráfica)
- Groq API + LLaMA 3.1 (geração de relatórios)
- PyMuPDF (leitura de PDFs)

# Como utilizar

1. Clone o repositório:
git clone https://github.com/vitu0972/Siria.git ou baixe o arquivo em 

2. Crie o ambiente virtual
python -m venv venv

## ativação da venv
Linux/Mac: source/venv/bin/activate
Windows: venv/Scripts/activate

3. Instale as dependências

pip install -r requisitos.txt