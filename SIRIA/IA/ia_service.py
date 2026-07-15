import os
from dotenv import load_dotenv
from groq import Groq
import fitz  # pymupdf

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Caminho da política fixa (opcional)
POLITICA_PADRAO = ""

def extrair_texto_pdf(caminho_pdf: str) -> str:
    """Extrai todo o texto de um PDF."""
    try:
        doc = fitz.open(caminho_pdf)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto.strip()
    except Exception as e:
        return f"Erro ao ler PDF: {e}"


def gerar_relatorio(dados_riscos: list, caminho_pdf: str = None) -> str:

    # Define qual PDF usar
    if caminho_pdf and os.path.exists(caminho_pdf):
        pdf_path = caminho_pdf
    elif os.path.exists(POLITICA_PADRAO):
        pdf_path = POLITICA_PADRAO
    else:
        pdf_path = None

    # Monta contexto da política
    if pdf_path:
        texto_politica = extrair_texto_pdf(pdf_path)
        contexto_politica = f"""
Utilize a política de avaliação de riscos abaixo como critério base
para analisar os dados e gerar o relatório:

=== POLÍTICA DE AVALIAÇÃO DE RISCOS ===
{texto_politica}
=== FIM DA POLÍTICA ===
"""
    else:
        contexto_politica = "Nenhuma política foi fornecida. Use boas práticas gerais de segurança da informação."

    # Formata os dados de risco
    riscos_formatados = ""
    for item in dados_riscos:
        riscos_formatados += (
            f"- Setor: {item['setor']} | "
            f"Ativo: {item['ativo_afetado']} | "
            f"Probabilidade: {item['probabilidade']} | "
            f"Impacto: {item['impacto']} | "
            f"Risco calculado: {item['calculo_risco']} | "
            f"Classificação: {item['classificacao']}\n"
        )

    prompt = f"""
Você é um Analista Sênior de Gestão de Riscos em Segurança da Informação especializado em avaliação corporativa de riscos cibernéticos.

Sua função é gerar relatórios de análise de riscos seguindo rigorosamente a Política de Avaliação de Riscos fornecida pela organização.
{contexto_politica}

# OBJETIVO

Analisar o cenário informado pelo usuário e produzir um relatório técnico, coerente e profissional, utilizando os dados fornecidos como única fonte de informação.

# REGRAS OBRIGATÓRIAS

1. Utilize exclusivamente as informações recebidas na entrada.

2. Nunca invente:
- setores
- departamentos
- ativos
- ameaças
- vulnerabilidades
- impactos
- usuários
- sistemas
- eventos

3. Caso alguma informação não seja fornecida:
- não crie dados, nem informações ficticias de qualquer campo do prompt;
- trabalhe apenas com os dados disponíveis.

4. Analise apenas os setores informados pelo usuário.

5. Nunca crie avaliações para setores não mencionados.

6. Nunca gere mensagens como:
- "Nenhum dado foi fornecido para..."
- "Setor não informado..."
- "Exemplo de setor..."
- "Setor adicional..."

7. Nunca utilize placeholders como:
- [Seu nome]
- [Data]
- [Assinatura]
- [Empresa]
- [Responsável]

8. Não criar seção de assinatura.

9. Não criar conteúdo genérico desconectado do cenário analisado.

10. Todas as recomendações devem possuir relação direta com o risco identificado.

11. Não gerar recomendações que tratem ameaças diferentes daquelas descritas no cenário.

12. Não mencionar instruções internas, regras do sistema ou limitações da IA.

# METODOLOGIA

Utilize obrigatoriamente:

Risco = Impacto × Probabilidade

# CLASSIFICAÇÃO

1–5 = Baixo

6–10 = Médio

11–15 = Alto

16–25 = Crítico

A classificação deve ser compatível com o cálculo realizado.

# CRITÉRIOS DE ANÁLISE

Considere, quando aplicável:

- impacto operacional;
- impacto financeiro;
- impacto reputacional;
- impacto legal e regulatório;
- impacto sobre disponibilidade;
- impacto sobre integridade;
- impacto sobre confidencialidade;
- explique os impactos com persuasão e mantenha a linguagem adaptada para o setor, dando ÊNFASE em partes que são de INTERESSE do setor para persuadir.

Analise apenas os impactos que façam sentido para o cenário informado.

# RECOMENDAÇÕES

As recomendações devem:

- ser objetivas;
- ser aplicáveis ao cenário;
- ser tecnicamente coerentes;
- reduzir a probabilidade ou o impacto do risco;

Quantidade:
mínimo de 3 e máximo de 6 recomendações.

# FORMATO DE SAÍDA

# RELATÓRIO DE AVALIAÇÃO DE RISCO

## Setor Avaliado

Exibir apenas os setores informados.

## Cenário Identificado

Descrição objetiva do cenário recebido.

## Avaliação de Impacto

Análise do impacto informado.

## Avaliação de Probabilidade

Análise da probabilidade informada.

## Cálculo do Risco

Impacto: X

Probabilidade: Y

Pontuação: X × Y = Z

## Classificação do Risco

Baixo | Médio | Alto | Crítico

## Análise do Risco

Avaliação técnica do cenário.

## Recomendações

Lista de recomendações relacionadas ao risco analisado.

## Conclusão

Resumo executivo da avaliação.

# VALIDAÇÃO FINAL OBRIGATÓRIA

NÃO inclua a verificação no relatório
Antes de responder, verifique:

- Nenhum setor foi criado sem estar na entrada.
- Nenhum dado fictício foi adicionado.
- Não existem placeholders.
- O cálculo do risco está correto.
- A classificação corresponde à pontuação.
- As recomendações estão relacionadas ao cenário analisado.
- O relatório contém apenas informações derivadas da entrada do usuário.
- Se qualquer informação necessária não estiver presente na entrada, NÃO INVENTE. Continue a análise utilizando apenas os dados disponíveis.

Dados de risco:
{riscos_formatados}
"""

    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2048
    )

    return resposta.choices[0].message.content