from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, Pegawai, Layanan, Pasien, Transaksi, DetailTransaksiLayanan, Produk, KategoriLayanan
import os
import secrets

# Import blueprints
from routes.pasien_routes import pasien_bp
from routes.pegawai_routes import pegawai_bp
from routes.layanan_routes import layanan_bp
from routes.produk_routes import produk_bp
from routes.transaksi_routes import transaksi_bp
from routes.kategori_layanan_routes import kategori_bp
from routes.layanan_pegawai_routes import layanan_pegawai_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://flaskuser:database_191025@RIFQI\\MSSQLSERVER01/MyFlaskDB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(pasien_bp)
app.register_blueprint(pegawai_bp)
app.register_blueprint(layanan_bp)
app.register_blueprint(produk_bp)
app.register_blueprint(transaksi_bp)
app.register_blueprint(kategori_bp)
app.register_blueprint(layanan_pegawai_bp)

with app.app_context():
    # Create tables if they don't exist
    db.create_all()
    
    # Create admin user if it doesn't exist
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('kategori.list_kategori'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('kategori.list_kategori'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Verify current password
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('change_password'))
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('change_password'))
        
        # Validate password length
        if len(new_password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('change_password'))
        
        # Update password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('kategori.list_kategori'))
    
    return render_template('change_password.html')

@app.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_username = request.form['new_username']
        
        # Verify current password
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('change_username'))
        
        # Validate username length
        if len(new_username) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return redirect(url_for('change_username'))
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Username already exists', 'error')
            return redirect(url_for('change_username'))
        
        # Update username
        current_user.username = new_username
        db.session.commit()
        flash('Username changed successfully!', 'success')
        return redirect(url_for('kategori.list_kategori'))
    
    return render_template('change_username.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        current_password = request.form.get('current_password')
        
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('profile'))
        
        if form_type == 'username':
            new_username = request.form.get('new_username')
            if User.query.filter_by(username=new_username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('profile'))
            
            current_user.username = new_username
            db.session.commit()
            flash('Username updated successfully', 'success')
            
        elif form_type == 'password':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'danger')
                return redirect(url_for('profile'))
            
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password updated successfully', 'success')
    
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True) 