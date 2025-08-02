import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="myportfolio_rrko",
        user="myportfolio_rrko_user",
        password="5Sjii0xnVw8IRU2oxJ9Qg3jeD57YO1Aa",
        host="dpg-d279gemuk2gs73dnf4p0-a",
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
   
