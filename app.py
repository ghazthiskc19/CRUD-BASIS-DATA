from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, Pegawai, Layanan, Pasien, Transaksi, DetailTransaksiLayanan, Produk, KategoriLayanan, DetailTransaksiProduk
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

# Context processor to inject stats into all templates
@app.context_processor
def inject_stats():
    if current_user.is_authenticated:
        from datetime import datetime, timedelta
        from sqlalchemy import func
        import calendar

        # Get current date
        now = datetime.now()
        
        # Initialize data for last 12 months
        revenue_data = []
        patient_data = []
        transaction_data = []
        for i in range(11, -1, -1):
            # Calculate start and end of month
            month_start = datetime(now.year, now.month, 1) - timedelta(days=i*30)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            monthly_revenue = db.session.query(
                func.sum(Transaksi.total_harga)
            ).filter(
                Transaksi.tanggal >= month_start,
                Transaksi.tanggal <= month_end
            ).scalar() or 0

            monthly_patients = db.session.query(
                func.count(Pasien.id_pasien)
            ).filter(
                Pasien.created_at >= month_start,
                Pasien.created_at <= month_end
            ).scalar() or 0

            monthly_transactions = db.session.query(
                func.count(Transaksi.id_transaksi)
            ).filter(
                Transaksi.tanggal >= month_start,
                Transaksi.tanggal <= month_end
            ).scalar() or 0

            # Add to revenue data
            revenue_data.append({
                'month': month_start.strftime('%b'),
                'revenue': float(monthly_revenue)
            })

            # Add to patient data
            patient_data.append({
                'month': month_start.strftime('%b'),
                'patients': monthly_patients
            })

            # Add to transaction data
            transaction_data.append({
                'month': month_start.strftime('%b'),
                'transactions': monthly_transactions
            })

        # Get top 3 most used services
        top_services = db.session.query(
            Layanan.nama_layanan,
            func.count(DetailTransaksiLayanan.id_layanan).label('total_used')
        ).join(
            DetailTransaksiLayanan,
            Layanan.id_layanan == DetailTransaksiLayanan.id_layanan
        ).group_by(
            Layanan.nama_layanan
        ).order_by(
            func.count(DetailTransaksiLayanan.id_layanan).desc()
        ).limit(3).all()

        # Get top 3 most used products
        top_products = db.session.query(
            Produk.nama_produk,
            func.count(DetailTransaksiProduk.id_produk).label('total_used')
        ).join(
            DetailTransaksiProduk,
            Produk.id_produk == DetailTransaksiProduk.id_produk
        ).group_by(
            Produk.nama_produk
        ).order_by(
            func.count(DetailTransaksiProduk.id_produk).desc()
        ).limit(3).all()

        stats = {
            'total_patients': Pasien.query.count(),
            'total_employees': Pegawai.query.count(),
            'total_services': Layanan.query.count(),
            'total_products': Produk.query.count(),
            'total_transactions': Transaksi.query.count(),
            'revenue_data': revenue_data,
            'patient_data': patient_data,
            'transaction_data': transaction_data,
            'top_services': [{'name': s[0], 'count': s[1]} for s in top_services],
            'top_products': [{'name': p[0], 'count': p[1]} for p in top_products]
        }
        return {'stats': stats}
    return {'stats': {}}

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

db.init_app(app)
with app.app_context():
    db.create_all()
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
        return render_template('dashboard.html', current_user=current_user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('dashboard.html', current_user=current_user)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return render_template('dashboard.html', current_user=current_user)
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
        return render_template('dashboard.html', current_user=current_user)
    
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
        return render_template('dashboard.html', current_user=current_user)
    
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