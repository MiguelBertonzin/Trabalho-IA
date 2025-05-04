import sqlite3
import math

# Função para calcular a similaridade entre o novo caso e o caso existente
def calcular_similaridade(caso_novo, caso_existente, pesos, limiares):
    diferenca_total = 0
    peso_total = 0

    for variavel, peso in pesos.items():
        if variavel != 'diagnostico':
            valor_novo = caso_novo[variavel]
            valor_existente = caso_existente[variavel]
            diferenca = abs(valor_novo - valor_existente)

            # Normaliza se houver limiar
            if variavel in limiares:
                diferenca_normalizada = diferenca / limiares[variavel]
                diferenca_normalizada = min(diferenca_normalizada, 1)
            else:
                diferenca_normalizada = diferenca

            diferenca_total += peso * diferenca_normalizada
            peso_total += peso

    if peso_total == 0:
        return 0  # evita divisão por zero
    similaridade = 1 - (diferenca_total / peso_total)
    return max(0, min(similaridade, 1))  # garante entre 0 e 1


# Função para buscar o caso mais semelhante no banco de dados
def buscar_e_comparar(cursor, caso_novo, pesos, limiares):
    # Busca todos os casos do banco
    cursor.execute("SELECT * FROM pacientes")
    casos_anteriores = cursor.fetchall()

    melhores_comparacoes = []

    for caso_existente in casos_anteriores:
        # Dados em ordem
        caso_existente_dict = { #"dicionário"
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
        similaridade = calcular_similaridade(caso_novo, caso_existente_dict, pesos, limiares)
        
        # Guardar a similaridade e o diagnóstico
        melhores_comparacoes.append((similaridade, caso_existente[15]))  # Incluindo o diagnóstico

    # Ordena pela maior similaridade (menor diferença)
    melhores_comparacoes.sort(key=lambda x: x[0], reverse=True)
    
    # Retorna o diagnóstico mais provável (caso mais semelhante)
    #return melhores_comparacoes[0][1]

    # Exibir os dois casos mais semelhantes
    print("\nCasos mais semelhantes encontrados:")
    for i in range(min(2, len(melhores_comparacoes))):
        #diferenca = melhores_comparacoes[i][0]
        #diagnostico = melhores_comparacoes[i][1]
        similaridade_pct = melhores_comparacoes[i][0] * 100
        print(f"{i+1}º mais semelhante: {melhores_comparacoes[i][1]} (Similaridade: {similaridade_pct:.2f}%)")

    return melhores_comparacoes[0][1]

# Função para inserir o novo caso no banco de dados
def inserir_novo_caso(cursor, conn, caso_novo):
    cursor.execute('''
        INSERT INTO pacientes (
            temp_corporea, dur_febre, idade, dor_articular, int_dor_articular, 
            dor_cabeca_freq, dor_cabeca_int, manchas, coceira, conjuntivite, 
            dor_musculo, edema_art, hipertrofia_ganglionar, plaquetas, diagnostico
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        caso_novo['temp_corporea'], caso_novo['dur_febre'], caso_novo['idade'], 
        caso_novo['dor_articular'], caso_novo['int_dor_articular'], 
        caso_novo['dor_cabeca_freq'], caso_novo['dor_cabeca_int'], 
        caso_novo['manchas'], caso_novo['coceira'], caso_novo['conjuntivite'], 
        caso_novo['dor_musculo'], caso_novo['edema_art'], caso_novo['hipertrofia_ganglionar'], 
        caso_novo['plaquetas'], caso_novo['diagnostico']
    ))

    conn.commit()
    print("Novo caso inserido no banco de dados com sucesso.")


# Função principal
def main():
    # Conectar ao banco
    conn = sqlite3.connect('doencas.db')
    cursor = conn.cursor()

    # Entrada de pesos definidos pelo usuário
    print("Informe os pesos (importância) para os sintomas abaixo (de 0 a 1):")
    peso_temp = float(input("Temperatura corporal: "))
    peso_musc = float(input("Dor muscular: "))
    peso_plaquetas = float(input("Plaquetas: "))

    # Definindo pesos das variáveis
    pesos = {
        'temp_corporea': peso_temp,  #0.8
        'dur_febre': 0.4,
        'idade': 0.2,
        'dor_articular': 0.6,
        'int_dor_articular': 0.8,
        'dor_cabeca_freq': 0.6,
        'dor_cabeca_int': 0.6,
        'manchas': 0.6,
        'coceira': 0.6,
        'conjuntivite': 0.4,
        'dor_musculo': peso_musc, #0.7
        'edema_art': 0.7,
        'hipertrofia_ganglionar': 0.7,
        'plaquetas': peso_plaquetas, #1
        'diagnostico': 0  # é a classificação
    }

    # Limiar de tolerância para normalização (valor aceitável de diferença)
    limiares = {
        'temp_corporea': 0.5,
        'dur_febre': 2,
        'idade': 5,
        'int_dor_articular': 2,
        'plaquetas': 20000
    }


    # Novo caso a ser comparado

    print("\nAgora, informe os sintomas do paciente:")

    caso_novo = {
        'temp_corporea': float(input("Temperatura corporal: ")),
        'dur_febre': int(input("Duração da febre (dias): ")),
        'idade': int(input("Idade: ")),
        'dor_articular': int(input("Tem dor articular? (0 = não, 1 = sim): ")),
        'int_dor_articular': int(input("Intensidade da dor articular (0 a 10): ")),
        'dor_cabeca_freq': int(input("Frequência da dor de cabeça (0 a 10): ")),
        'dor_cabeca_int': int(input("Intensidade da dor de cabeça (0 a 10): ")),
        'manchas': int(input("Tem manchas na pele? (0 = não, 1 = sim): ")),
        'coceira': int(input("Tem coceira? (0 = não, 1 = sim): ")),
        'conjuntivite': int(input("Tem conjuntivite? (0 = não, 1 = sim): ")),
        'dor_musculo': int(input("Tem dor muscular? (0 = não, 1 = sim): ")),
        'edema_art': int(input("Tem edema articular? (0 = não, 1 = sim): ")),
        'hipertrofia_ganglionar': int(input("Tem hipertrofia ganglionar? (0 = não, 1 = sim): ")),
        'plaquetas': int(input("Número de plaquetas: ")),
        'diagnostico': ''
    }

    # Buscar o diagnóstico mais provável
    diagnostico_previsto = buscar_e_comparar(cursor, caso_novo, pesos, limiares)

    print(f"O diagnóstico mais provável é: {diagnostico_previsto}")

    diagnostico_real = input("Informe o diagnóstico real (Dengue, Zika, Chikungunya): ").strip().capitalize()
    caso_novo['diagnostico'] = diagnostico_real

    inserir_novo_caso(cursor, conn, caso_novo)

    # Fecha a conexão
    conn.close()

# Chama a função principal
if __name__ == "__main__":
    main()

#exemplo de caso
#caso_novo = {
     #   'temp_corporea': 37.5,
     #  'dur_febre': 5,
     #   'idade': 27,
     #   'dor_articular': 1,
     #   'int_dor_articular': 6,
     #   'dor_cabeca_freq': 4,
     #   'dor_cabeca_int': 5,
     #   'manchas': 1,
     #   'coceira': 1,
     #   'conjuntivite': 0,
     #   'dor_musculo': 1,
     #   'edema_art': 0,
     #   'hipertrofia_ganglionar': 1,
     #   'plaquetas': 180000,
     #   'diagnostico': ''  # Queremos prever
    #}
