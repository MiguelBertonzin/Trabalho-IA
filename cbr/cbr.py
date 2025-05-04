import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
import os

# Função para carregar os dados do banco
def carregar_casos():
    caminho = os.path.abspath('doencas.db')
    print(f"📍 Acessando banco em: {caminho}")

    conn = sqlite3.connect('doencas.db')
    df = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    return df

# Função principal de raciocínio baseado em casos
def prever_diagnostico(novo_caso):
    dados = carregar_casos()

    # Seleciona os atributos de entrada (sem o diagnóstico)
    X = dados[['febre', 'dor_articular', 'manchas', 'coceira', 'conjuntivite', 'plaquetas']]
    y = dados['diagnostico']

    # Novo caso como DataFrame
    novo_df = pd.DataFrame([novo_caso])

    # Cálculo da distância euclidiana
    distancias = euclidean_distances(X, novo_df)
    indice_similar = distancias.argmin()

    # Retorna o diagnóstico mais próximo
    return y.iloc[indice_similar]

# Executar vários testes simulados
if __name__ == '__main__':
    casos_teste = [
        {
            'nome': 'Caso 1 (suspeita de Zika)',
            'dados': {
                'febre': 1,
                'dor_articular': 0,
                'manchas': 1,
                'coceira': 1,
                'conjuntivite': 1,
                'plaquetas': 160000
            }
        },
        {
            'nome': 'Caso 2 (suspeita de Dengue)',
            'dados': {
                'febre': 1,
                'dor_articular': 1,
                'manchas': 0,
                'coceira': 0,
                'conjuntivite': 0,
                'plaquetas': 125000
            }
        },
        {
            'nome': 'Caso 3 (suspeita de Chikungunya)',
            'dados': {
                'febre': 1,
                'dor_articular': 1,
                'manchas': 0,
                'coceira': 0,
                'conjuntivite': 0,
                'plaquetas': 210000
            }
        },
        {
            'nome': 'Caso 4 (caso leve, possível Zika)',
            'dados': {
                'febre': 0,
                'dor_articular': 0,
                'manchas': 1,
                'coceira': 1,
                'conjuntivite': 1,
                'plaquetas': 175000
            }
        },
        {
            'nome': 'Caso 5 (caso ambíguo)',
            'dados': {
                'febre': 1,
                'dor_articular': 1,
                'manchas': 1,
                'coceira': 1,
                'conjuntivite': 0,
                'plaquetas': 150000
            }
        }
    ]

    # Executar os testes
    for caso in casos_teste:
        resultado = prever_diagnostico(caso['dados'])
        print(f"🧪 {caso['nome']}: Diagnóstico sugerido → {resultado}")
