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

    # Usa as mesmas colunas do banco
    colunas = ['temp_corporea', 'dur_febre', 'idade', 'dor_articular', 'int_dor_articular',
               'dor_cabeca_freq', 'dor_cabeca_int', 'manchas', 'coceira', 'conjuntivite',
               'dor_musculo', 'edema_art', 'hipertrofia_ganglionar', 'plaquetas']

    X = dados[colunas]
    y = dados['diagnostico']

    novo_df = pd.DataFrame([novo_caso])[colunas]

    distancias = euclidean_distances(X, novo_df)
    indice_similar = distancias.argmin()

    return y.iloc[indice_similar]

# Casos de teste
if __name__ == '__main__':
    casos_teste = [
        {
            'nome': 'Caso 1 (suspeita de Zika)',
            'dados': {
                'temp_corporea': 37.4,
                'dur_febre': 4,
                'idade': 29,
                'dor_articular': 0,
                'int_dor_articular': 0,
                'dor_cabeca_freq': 5,
                'dor_cabeca_int': 5,
                'manchas': 1,
                'coceira': 1,
                'conjuntivite': 1,
                'dor_musculo': 0,
                'edema_art': 0,
                'hipertrofia_ganglionar': 1,
                'plaquetas': 165000
            }
        },
        {
            'nome': 'Caso 2 (suspeita de Dengue)',
            'dados': {
                'temp_corporea': 38.5,
                'dur_febre': 6,
                'idade': 21,
                'dor_articular': 1,
                'int_dor_articular': 8,
                'dor_cabeca_freq': 6,
                'dor_cabeca_int': 7,
                'manchas': 0,
                'coceira': 0,
                'conjuntivite': 0,
                'dor_musculo': 1,
                'edema_art': 0,
                'hipertrofia_ganglionar': 0,
                'plaquetas': 130000
            }
        },
        {
            'nome': 'Caso 3 (suspeita de Chikungunya)',
            'dados': {
                'temp_corporea': 38.0,
                'dur_febre': 3,
                'idade': 33,
                'dor_articular': 1,
                'int_dor_articular': 9,
                'dor_cabeca_freq': 3,
                'dor_cabeca_int': 4,
                'manchas': 1,
                'coceira': 0,
                'conjuntivite': 0,
                'dor_musculo': 1,
                'edema_art': 1,
                'hipertrofia_ganglionar': 1,
                'plaquetas': 190000
            }
        }
    ]

    # Executar os testes
    for caso in casos_teste:
        resultado = prever_diagnostico(caso['dados'])
        print(f"🧪 {caso['nome']}: Diagnóstico sugerido → {resultado}")
