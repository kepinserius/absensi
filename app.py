from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'secret_key_for_session_management'  # Ubah dengan kunci rahasia Anda

# Konfigurasi koneksi ke database PostgreSQL
DB_CONFIG = {
    'dbname': 'absensi',
    'user': 'postgres',        # Ganti dengan username PostgreSQL Anda
    'password': 'password123', # Ganti dengan password PostgreSQL Anda
    'host': 'localhost',
    'port': '5432'
}

# Fungsi untuk membuat koneksi ke database
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Halaman login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Periksa pengguna di database
        cur.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if user:
            session['username'] = username
            session['role'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return render_template('error.html', message="Username atau password salah.")
    
    return render_template('login.html')

# Halaman dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    if role == 'admin':
        return render_template('dashboard.html', message="Selamat datang, Admin!")
    elif role == 'employee':
        return render_template('dashboard.html', message="Selamat datang, Karyawan!")
    else:
        return render_template('error.html', message="Role tidak dikenal.")

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
