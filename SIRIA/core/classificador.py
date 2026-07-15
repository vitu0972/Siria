import json
import os

def classificar_risco(valor):

    if valor <= 5:
        return 'Baixo'
    
    if valor <= 10:
        return 'Médio'
    
    if valor <= 15:
        return 'Alto'
    
    if valor <= 25:
        return 'Crítico'
    
    return 'Indefinido'
    
def salvar_json(dados):

    arquivo = 'riscos.json'

    lista = []

    # verifica se os arquivos já existe
    if os.path.exists(arquivo):

        with open(arquivo, "r", encoding='utf-8') as f:
            try:
                lista = json.load(f)
            except:
                lista = []
        
    # adiciona novo risco
    lista.append(dados)

    # salva novamente
    with open(arquivo, "w", encoding='utf-8') as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)