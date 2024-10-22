import sqlite3

def create_database():
    conn = sqlite3.connect('finanzas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY,
            fecha TEXT,
            descripcion TEXT,
            categoria TEXT,
            monto REAL
        )
    ''')
    conn.commit()
    conn.close()

create_database()
