import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="myportfolio",
        user="postgres",
        password="At@290519*",
        host="localhost",
        port="5432"
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(250),
    email VARCHAR(250) UNIQUE,
    password TEXT,
    created_date DATE
    );
''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(250),
            email VARCHAR(250),
            message TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')


    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    init_db()
   
