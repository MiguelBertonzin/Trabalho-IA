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
casos = [ #faltam casos
    (36.5, 7, 25, 1, 8, 6, 5, 4, 1, 1, 0, 1, 0, 200000, 'Dengue'),
    (37.8, 5, 30, 1, 9, 7, 8, 6, 0, 0, 1, 1, 1, 180000, 'Zika'),
    (38.2, 3, 40, 1, 7, 5, 7, 3, 1, 1, 1, 0, 1, 220000, 'Chikungunya'),
    (37.0, 10, 22, 1, 6, 8, 5, 2, 0, 1, 1, 1, 0, 160000, 'Dengue'),
    (36.7, 4, 28, 0, 5, 6, 6, 4, 1, 1, 0, 1, 1, 150000, 'Chikungunya'),
    (38.5, 6, 24, 1, 8, 7, 9, 6, 0, 1, 1, 1, 1, 170000, 'Zika'),
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
