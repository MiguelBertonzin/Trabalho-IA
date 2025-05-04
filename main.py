#Trabalho M2 Inteligência Artificial
#Alunos Julia Coelho Rodrigues e Miguel Bertonzin.
import sqlite3


# Função para calcular a similaridade entre o novo caso e o caso existente
def calcular_similaridade(caso_novo, caso_existente, pesos):
    similaridade = 0
    for variavel, peso in pesos.items():
        if variavel != 'diagnostico':  # Não compara o diagnóstico
            valor_novo = caso_novo[variavel]
            valor_existente = caso_existente[variavel]

            # Aqui você pode usar uma fórmula de diferença simples (exemplo: diferença absoluta)
            similaridade += peso * abs(valor_novo - valor_existente)

    return similaridade


# Função para buscar o caso mais semelhante no banco de dados
def buscar_e_comparar(cursor, caso_novo, pesos):
    # Busca todos os casos do banco
    cursor.execute("SELECT * FROM pacientes")
    casos_anteriores = cursor.fetchall()

    melhores_comparacoes = []

    for caso_existente in casos_anteriores:
        # Dados em ordem
        caso_existente_dict = {
            'temp_corporea': caso_existente[1],
            'dur_febre': caso_existente[2],
            'idade': caso_existente[3],
            'dor_articular': caso_existente[4],
            'int_dor_articular': caso_existente[5],
            'dor_cabeca_freq': caso_existente[6],
            'dor_cabeca_int': caso_existente[7],
            'manchas': caso_existente[8],
            'coceira': caso_existente[9],
            'conjuntivite': caso_existente[10],
            'dor_musculo': caso_existente[11],
            'edema_art': caso_existente[12],
            'hipertrofia_ganglionar': caso_existente[13],
            'plaquetas': caso_existente[14],
            'diagnostico': caso_existente[15]
        }

        # Comparar o novo caso com o caso existente
        similaridade = calcular_similaridade(caso_novo, caso_existente_dict, pesos)

        # Guardar a similaridade e o diagnóstico
        melhores_comparacoes.append((similaridade, caso_existente[15]))  # Incluindo o diagnóstico

    # Ordena pela maior similaridade (menor diferença)
    melhores_comparacoes.sort(key=lambda x: x[0])

    # Retorna o diagnóstico mais provável (caso mais semelhante)
    return melhores_comparacoes[0][1]


# Função principal
def main():
    # Conectar ao banco
    conn = sqlite3.connect('doencas.db')
    cursor = conn.cursor()

    # Definindo pesos das variáveis
    pesos = {
        'temp_corporea': 0.8,
        'dur_febre': 0.4,
        'idade': 0.2,
        'dor_articular': 0.6,
        'int_dor_articular': 0.8,
        'dor_cabeca_freq': 0.6,
        'dor_cabeca_int': 0.6,
        'manchas': 0.6,
        'coceira': 0.6,
        'conjuntivite': 0.4,
        'dor_musculo': 0.7,
        'edema_art': 0.7,
        'hipertrofia_ganglionar': 0.7,
        'plaquetas': 1,
        'diagnostico': 0  # é a classificação
    }

    # Exemplo de um novo caso a ser comparado
    caso_novo = {
        'temp_corporea': 37.5,
        'dur_febre': 5,
        'idade': 27,
        'dor_articular': 1,
        'int_dor_articular': 6,
        'dor_cabeca_freq': 4,
        'dor_cabeca_int': 5,
        'manchas': 1,
        'coceira': 1,
        'conjuntivite': 0,
        'dor_musculo': 1,
        'edema_art': 0,
        'hipertrofia_ganglionar': 1,
        'plaquetas': 180000,
        'diagnostico': ''  # O diagnóstico é o que queremos prever
    }

    # Buscar o diagnóstico mais provável
    diagnostico_previsto = buscar_e_comparar(cursor, caso_novo, pesos)

    print(f"O diagnóstico mais provável é: {diagnostico_previsto}")

    # Fecha a conexão
    conn.close()


# Chama a função principal
if __name__ == "__main__":
    main()
