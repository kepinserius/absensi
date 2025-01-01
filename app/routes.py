from flask import render_template, request, redirect, url_for, session, flash
from app import app
from werkzeug.security import check_password_hash
import psycopg2

# Koneksi ke database PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="absensi",
        user="postgres",
        password="password"  # Ganti dengan password PostgreSQL Anda
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Koneksi ke database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Ambil user dari database berdasarkan username
        cur.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if user:
            user_id, hashed_password, role = user
            if check_password_hash(hashed_password, password):  # Validasi password
                session['user_id'] = user_id
                session['username'] = username
                session['role'] = role
                flash('Login berhasil!', 'success')
                
                # Arahkan ke dashboard berdasarkan peran
                if role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif role == 'karyawan':
                    return redirect(url_for('karyawan_dashboard'))
            else:
                flash('Password salah!', 'danger')
        else:
            flash('Username tidak ditemukan!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Hapus sesi pengguna
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Akses ditolak. Anda bukan admin.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/dashboard/karyawan')
def karyawan_dashboard():
    if session.get('role') != 'karyawan':
        flash('Akses ditolak. Anda bukan karyawan.', 'danger')
        return redirect(url_for('login'))
    return render_template('karyawan_dashboard.html')
