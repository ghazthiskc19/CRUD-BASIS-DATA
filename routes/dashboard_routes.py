from flask import Blueprint, render_template
from flask_login import login_required
from models import Pasien, Pegawai, Layanan, Produk, Transaksi, DetailTransaksiLayanan, DetailTransaksiProduk
from database import db
from datetime import datetime, timedelta
from sqlalchemy import func
from decimal import Decimal

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Get total counts
    total_patients = Pasien.query.count()
    total_employees = Pegawai.query.count()
    total_services = Layanan.query.count()
    total_products = Produk.query.count()
    total_transactions = Transaksi.query.count()

    # Get patient trend data (last 12 months)
    patient_data = []
    for i in range(11, -1, -1):
        date = datetime.now() - timedelta(days=30*i)
        month = date.strftime('%Y-%m')
        count = Pasien.query.filter(
            func.date_format(Pasien.tanggal_daftar, '%Y-%m') == month
        ).count()
        patient_data.append({
            'month': date.strftime('%b %Y'),
            'patients': count
        })

    # Get revenue trend data (last 12 months)
    revenue_data = []
    for i in range(11, -1, -1):
        date = datetime.now() - timedelta(days=30*i)
        month = date.strftime('%Y-%m')
        revenue = db.session.query(func.sum(Transaksi.total_harga)).filter(
            func.date_format(Transaksi.tanggal, '%Y-%m') == month
        ).scalar() or Decimal('0')
        revenue_data.append({
            'month': date.strftime('%b %Y'),
            'revenue': float(revenue)
        })

    # Get transaction trend data (last 12 months)
    transaction_data = []
    for i in range(11, -1, -1):
        date = datetime.now() - timedelta(days=30*i)
        month = date.strftime('%Y-%m')
        count = Transaksi.query.filter(
            func.date_format(Transaksi.tanggal, '%Y-%m') == month
        ).count()
        transaction_data.append({
            'month': date.strftime('%b %Y'),
            'transactions': count
        })

    # Get top services
    top_services = db.session.query(
        Layanan.nama_layanan,
        func.count(DetailTransaksiLayanan.id_detailLayanan).label('count')
    ).join(DetailTransaksiLayanan).group_by(Layanan.nama_layanan).order_by(
        func.count(DetailTransaksiLayanan.id_detailLayanan).desc()
    ).limit(3).all()
    
    top_services_data = [{
        'name': service[0],
        'count': service[1]
    } for service in top_services]

    # Get top products
    top_products = db.session.query(
        Produk.nama_produk,
        func.count(DetailTransaksiProduk.id_detailProduk).label('count')
    ).join(DetailTransaksiProduk).group_by(Produk.nama_produk).order_by(
        func.count(DetailTransaksiProduk.id_detailProduk).desc()
    ).limit(3).all()
    
    top_products_data = [{
        'name': product[0],
        'count': product[1]
    } for product in top_products]

    stats = {
        'total_patients': total_patients,
        'total_employees': total_employees,
        'total_services': total_services,
        'total_products': total_products,
        'total_transactions': total_transactions,
        'patient_data': patient_data,
        'revenue_data': revenue_data,
        'transaction_data': transaction_data,
        'top_services': top_services_data,
        'top_products': top_products_data
    }

    return render_template('dashboard.html', stats=stats) 