import sqlite3

# Conectar ao banco
conn = sqlite3.connect('doencas.db')
cursor = conn.cursor()

# Força recriação da tabela
cursor.execute('DROP TABLE IF EXISTS pacientes')

# Cria a tabela
cursor.execute('''
CREATE TABLE pacientes (
    id INTEGER PRIMARY KEY,
    temp_corporea REAL,
    dur_febre INTEGER,
    idade REAL,
    dor_articular INTEGER,
    int_dor_articular INTEGER,
    dor_cabeca_freq INTEGER,
    dor_cabeca_int INTEGER,
    manchas INTEGER,
    coceira INTEGER,
    conjuntivite INTEGER,
    dor_musculo INTEGER,
    edema_art INTEGER,
    hipertrofia_ganglionar INTEGER,
    plaquetas INTEGER,
    diagnostico TEXT
)
''')

# Insere casos
casos = [ #18 casos + 3 atípicos
    (36.5, 7, 25, 1, 8, 6, 5, 1, 1, 1, 0, 1, 0, 200000, 'Dengue'),
    (37.0, 10, 22, 1, 6, 8, 5, 1, 0, 1, 1, 1, 0, 160000, 'Dengue'),
    (39.0, 3, 30, 1, 8, 7, 6, 0, 0, 0, 1, 0, 0, 140000, 'Dengue'),
    (39.5, 6, 40, 0, 0, 8, 7, 0, 0, 0, 1, 0, 0, 110000, 'Dengue'),
    (39.1, 5, 33, 1, 7, 6, 6, 0, 0, 0, 1, 1, 0, 120000, 'Dengue'),
    (39.2, 6, 31, 1, 8, 7, 7, 0, 0, 0, 1, 0, 0, 100000, 'Dengue'),
    (37.8, 5, 30, 1, 9, 7, 8, 1, 0, 0, 1, 1, 1, 180000, 'Zika'),
    (38.5, 6, 24, 1, 8, 7, 9, 1, 0, 1, 1, 1, 1, 170000, 'Zika'),
    (38.5, 4, 25, 1, 7, 6, 5, 1, 1, 0, 1, 0, 1, 150000, 'Zika'),
    (38.2, 2, 35, 1, 4, 3, 4, 1, 0, 1, 1, 0, 0, 200000, 'Zika'),
    (37.2, 3, 19, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 250000, 'Zika'),
    (38.3, 3, 24, 1, 5, 5, 5, 1, 1, 1, 1, 0, 0, 190000, 'Zika'),
    (38.2, 3, 40, 1, 7, 5, 7, 1, 1, 1, 1, 0, 1, 220000, 'Chikungunya'),
    (36.7, 4, 28, 0, 5, 6, 6, 1, 1, 1, 0, 1, 1, 150000, 'Chikungunya'),
    (37.8, 5, 22, 1, 6, 4, 5, 1, 1, 1, 1, 1, 1, 180000, 'Chikungunya'),
    (38.0, 4, 28, 1, 9, 5, 4, 1, 1, 0, 1, 1, 1, 160000, 'Chikungunya'),
    (37.9, 4, 27, 1, 6, 5, 4, 1, 1, 1, 1, 1, 1, 170000, 'Chikungunya'),
    (38.1, 4, 26, 1, 9, 6, 6, 1, 1, 1, 1, 1, 1, 155000, 'Chikungunya'),
    #casos atipicos
    (36.0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 300000, 'Zika'),  # Quase assintomático, plaquetas altas
    (39.8, 7, 32, 1, 10, 9, 9, 1, 2, 2, 2, 2, 2, 90000, 'Dengue'),  # Caso grave com sintomas intensos e plaquetas muito baixas
    (37.5, 1, 60, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 200000, 'Chikungunya'),  # Idoso, início da febre, sintomas leves e articulações afetadas
]

cursor.executemany('''
INSERT INTO pacientes (temp_corporea, dur_febre, idade, dor_articular, int_dor_articular, 
dor_cabeca_freq, dor_cabeca_int, manchas, coceira, conjuntivite, dor_musculo, edema_art, 
hipertrofia_ganglionar, plaquetas, diagnostico)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', casos)

conn.commit()
conn.close()

print("Banco criado e populado com sucesso.")
