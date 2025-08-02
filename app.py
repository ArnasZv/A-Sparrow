from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection, init_db
from flask_cors import CORS
from flask import jsonify
from datetime import datetime



app = Flask(__name__)
CORS(app)
app.secret_key = '290519'

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about_me.html')
def about_me():
    return render_template('about_me.html')

@app.route('/contact_me.html')
def contact_me():
    return render_template('contact_me.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home')) #<-- Redirect to home
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route('/api/users/signup', methods=['POST'])
def api_register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    created_date = data.get('created_date', datetime.today().date())

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO users (username, email, password, created_date)
            VALUES (%s, %s, %s, %s)
        ''', (username, email, password, created_date))
        conn.commit()
        
        flash('You have registered successfully!', 'success')  # ✅ Flash message
        return jsonify({'redirect_url': url_for('login')}), 201  # Send redirect URL to JS

    except Exception as e:
        conn.rollback()
        return str(e), 400
    finally:
        cur.close()
        conn.close()


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return jsonify({'message': 'Login successful! Redirecting...'}), 200
    else:
        return jsonify({'message': 'Invalid email or password.'}), 401
    
@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO contact_messages (name, email, message)
                VALUES (%s, %s, %s)
            ''', (name, email, message))
            conn.commit()
            flash('Thank you for contacting us, We will get back to you as soon as possible.!')
        except Exception as e:
            conn.rollback()
            flash(f"Something went wrong: {str(e)}", 'danger')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('contact_me'))
    
    

if __name__ == '__main__':
    app.run(host= '0.0.0.0' , debug=True)