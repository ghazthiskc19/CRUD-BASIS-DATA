from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_login import login_required
from models import Transaksi, DetailTransaksiLayanan, DetailTransaksiProduk, Pasien, Layanan, Produk, Pegawai, LayananPegawai
from database import db
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import String
from decimal import Decimal
from flask import current_app
import csv
import io

transaksi_bp = Blueprint('transaksi', __name__)

@transaksi_bp.route('/transaksi')
@login_required
def list_transaksi():
    transaksi_list = Transaksi.query.all()
    pegawai_list = Pegawai.query.all()
    
    pegawai_data = [
        {
            'id_pegawai': p.id_pegawai,
            'nama': p.nama
        }
        for p in pegawai_list
    ]
    return render_template('transaksi.html', 
                         action='list', 
                         transaksi_list=transaksi_list,
                         pegawai_list=pegawai_data) 

@transaksi_bp.route('/transaksi/add', methods=['GET', 'POST'])
@login_required
def add_transaksi():
    if request.method == 'POST':
        try:
            if not request.form.get('id_pasien'):
                raise ValueError("Pasien harus dipilih")
            
            with db.session.begin_nested():
                transaksi = Transaksi(
                    id_pasien=request.form['id_pasien'],
                    tanggal=date.today(),
                    total_harga=Decimal('0')  # Will be calculated after adding details
                )
                db.session.add(transaksi)
                db.session.flush()  # Get the transaksi ID without committing

                total_harga = Decimal('0')

                layanan_ids = request.form.getlist('layanan_ids[]')
                pegawai_ids = request.form.getlist('pegawai_ids[]')
                kuantitas_layanan = request.form.getlist('kuantitas_layanan[]')
                
                if not layanan_ids:
                    raise ValueError("Transaksi harus memiliki minimal satu layanan")
                
                for i in range(len(layanan_ids)):
                    if not layanan_ids[i] or not pegawai_ids[i] or not kuantitas_layanan[i]:
                        raise ValueError("Semua field layanan harus diisi")
                    
                    try:
                        kuantitas = int(kuantitas_layanan[i])
                        if kuantitas <= 0:
                            raise ValueError("Kuantitas layanan harus lebih dari 0")
                    except ValueError:
                        raise ValueError("Format kuantitas layanan tidak valid")
                    
                    layanan = Layanan.query.get(layanan_ids[i])
                    pegawai = Pegawai.query.get(pegawai_ids[i])
                    
                    if not layanan or not pegawai:
                        raise ValueError("Layanan atau pegawai tidak ditemukan")
                    
                    layanan_pegawai = db.session.query(LayananPegawai).filter_by(
                        id_layanan=layanan_ids[i],
                        id_pegawai=pegawai_ids[i]
                    ).first()
                    
                    if not layanan_pegawai:
                        raise ValueError(f"Pegawai {pegawai.nama} tidak terdaftar untuk layanan {layanan.nama_layanan}")
                    
                    subtotal = layanan_pegawai.biaya * Decimal(str(kuantitas))
                    total_harga += subtotal
                    
                    detail = DetailTransaksiLayanan(
                        id_transaksi=transaksi.id_transaksi,
                        id_pegawai=pegawai_ids[i],
                        id_layanan=layanan_ids[i],
                        kuantitas=kuantitas,
                        subtotal=subtotal
                    )
                    db.session.add(detail)

                produk_ids = request.form.getlist('produk_ids[]')
                kuantitas_produk = request.form.getlist('kuantitas_produk[]')
                
                if any(produk_ids):
                    for i in range(len(produk_ids)):
                        if produk_ids[i] and kuantitas_produk[i]:  # Only process if both fields are filled
                            try:
                                kuantitas = int(kuantitas_produk[i])
                                if kuantitas <= 0:
                                    raise ValueError("Kuantitas produk harus lebih dari 0")
                            except ValueError:
                                raise ValueError("Format kuantitas produk tidak valid")
                            
                            produk = Produk.query.get(produk_ids[i])
                            if not produk:
                                raise ValueError("Produk tidak ditemukan")
                            
                            if produk.stok < kuantitas:
                                raise ValueError(f"Stok produk {produk.nama_produk} tidak mencukupi")
                            
                            subtotal = produk.harga * Decimal(str(kuantitas))
                            total_harga += subtotal
                            
                            # Update product stock
                            produk.stok -= kuantitas
                            
                            detail = DetailTransaksiProduk(
                                id_transaksi=transaksi.id_transaksi,
                                id_produk=produk_ids[i],
                                kuantitas=kuantitas,
                                subtotal=subtotal
                            )
                            db.session.add(detail)

                transaksi.total_harga = total_harga
            
            db.session.commit()
            flash('Transaksi berhasil ditambahkan!', 'success')
            return redirect(url_for('transaksi.list_transaksi'))
            
        except ValueError as ve:
            db.session.rollback()
            flash(f'Error validasi: {str(ve)}', 'error')
        except IntegrityError as ie:
            db.session.rollback()
            flash('Error: Terjadi kesalahan integritas data', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('transaksi.add_transaksi'))
    
    pasien_list = Pasien.query.all()
    layanan_list = Layanan.query.all()
    produk_list = Produk.query.all()
    pegawai_list = Pegawai.query.all()
    
    # Convert layanan_pegawai data to a serializable format
    for layanan in layanan_list:
        layanan.layanan_pegawai_data = [
            {
                'id_pegawai': lp.id_pegawai,
                'biaya': float(lp.biaya)
            }
            for lp in layanan.layanan_pegawai
        ]
    
    # Convert pegawai_list to a serializable format
    pegawai_data = [
        {
            'id_pegawai': p.id_pegawai,
            'nama': p.nama
        }
        for p in pegawai_list
    ]
    
    print("Debug - Pegawai Data:", pegawai_data)  # Debug print
    
    return render_template('transaksi.html', 
                         action='add',
                         pasien_list=pasien_list,
                         layanan_list=layanan_list,
                         produk_list=produk_list,
                         pegawai_list=pegawai_data)

@transaksi_bp.route('/transaksi/view/<int:id_transaksi>')
@login_required
def view_transaksi(id_transaksi):
    transaksi = Transaksi.query.get_or_404(id_transaksi)
    detail_layanan = DetailTransaksiLayanan.query.filter_by(id_transaksi=id_transaksi).all()
    detail_produk = DetailTransaksiProduk.query.filter_by(id_transaksi=id_transaksi).all()
    pegawai_list = Pegawai.query.all()
    
    # Convert pegawai_list to a serializable format
    pegawai_data = [
        {
            'id_pegawai': p.id_pegawai,
            'nama': p.nama
        }
        for p in pegawai_list
    ]
    
    return render_template('transaksi.html',
                         transaksi=transaksi,
                         detail_layanan=detail_layanan,
                         detail_produk=detail_produk,
                         pegawai_list=pegawai_data,
                         action='view')

@transaksi_bp.route('/transaksi/delete/<int:id_transaksi>', methods=['POST'])
@login_required
def delete_transaksi(id_transaksi):
    transaksi = Transaksi.query.get_or_404(id_transaksi)
    try:
        with db.session.begin_nested():
            # Restore product stock
            detail_produk = DetailTransaksiProduk.query.filter_by(id_transaksi=id_transaksi).all()
            for detail in detail_produk:
                produk = Produk.query.get(detail.id_produk)
                if produk:
                    produk.stok += detail.kuantitas
            
            db.session.delete(transaksi)
        
        db.session.commit()
        flash('Transaksi berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('transaksi.list_transaksi'))

@transaksi_bp.route('/transaksi/live_search')
@login_required
def live_search():
    try:
        query_param = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all')  # 'all', 'pasien', 'tanggal', 'bulan', 'id'
        
        if not query_param:
            list_transaksi = Transaksi.query.all()
        else:
            base_query = Transaksi.query.join(Pasien)
            
            if search_type == 'all':
                # Search in all fields
                list_transaksi = base_query.filter(
                    (Pasien.nama.ilike(f"%{query_param}%")) |
                    (Transaksi.id_transaksi.cast(String).ilike(f"%{query_param}%")) |
                    (Transaksi.tanggal.cast(String).ilike(f"%{query_param}%"))
                ).all()
            elif search_type == 'pasien':
                # Search by patient name
                list_transaksi = base_query.filter(
                    Pasien.nama.ilike(f"%{query_param}%")
                ).all()
            elif search_type == 'tanggal':
                # Search by date
                try:
                    search_date = datetime.strptime(query_param, '%Y-%m-%d').date()
                    list_transaksi = base_query.filter(
                        Transaksi.tanggal == search_date
                    ).all()
                except ValueError:
                    list_transaksi = []
            elif search_type == 'bulan':
                # Search by month
                try:
                    # Parse the month input (format: YYYY-MM)
                    year, month = map(int, query_param.split('-'))
                    # Get the first and last day of the month
                    first_day = date(year, month, 1)
                    if month == 12:
                        last_day = date(year + 1, 1, 1) - timedelta(days=1)
                    else:
                        last_day = date(year, month + 1, 1) - timedelta(days=1)
                    
                    list_transaksi = base_query.filter(
                        Transaksi.tanggal.between(first_day, last_day)
                    ).all()
                except ValueError:
                    list_transaksi = []
            elif search_type == 'id':
                # Search by transaction ID
                try:
                    transaksi_id = int(query_param)
                    list_transaksi = base_query.filter(
                        Transaksi.id_transaksi == transaksi_id
                    ).all()
                except ValueError:
                    list_transaksi = []
            else:
                list_transaksi = []

        results = [{
            'id_transaksi': transaksi.id_transaksi,
            'tanggal': transaksi.tanggal.strftime('%Y-%m-%d'),
            'nama_pasien': transaksi.pasien.nama,
            'total_harga': float(transaksi.total_harga)
        } for transaksi in list_transaksi]
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error in live_search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 

@transaksi_bp.route('/transaksi/export_csv')
@login_required
def export_csv():
    try:
        # Load transactions with all related data
        all_transaksi = Transaksi.query.options(
            db.joinedload(Transaksi.pasien),
            db.joinedload(Transaksi.detail_transaksi_layanan).joinedload(DetailTransaksiLayanan.layanan),
            db.joinedload(Transaksi.detail_transaksi_layanan).joinedload(DetailTransaksiLayanan.pegawai),
            db.joinedload(Transaksi.detail_transaksi_produk).joinedload(DetailTransaksiProduk.produk)
        ).all()

        if not all_transaksi:
            flash('Tidak ada data yang dapat di export.', 'info')
            return redirect(url_for('.list_transaksi'))
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            'ID Transaksi', 'Tanggal', 'Nama Pasien', 'Total Harga',
            'Tipe Detail', 'ID Detail', 'Nama Item', 'Pegawai', 'Kuantitas', 'Subtotal'
        ])

        # Write all transaction details
        for transaksi in all_transaksi:
            # Common transaction data
            base_data = [
                transaksi.id_transaksi,
                transaksi.tanggal.strftime('%Y-%m-%d'),
                transaksi.pasien.nama,
                float(transaksi.total_harga)
            ]
            
            # Write service details
            for detail in transaksi.detail_transaksi_layanan:
                writer.writerow(base_data + [
                    'Layanan',
                    detail.id_detailLayanan,
                    detail.layanan.nama_layanan,
                    detail.pegawai.nama,
                    detail.kuantitas,
                    float(detail.subtotal)
                ])
            
            # Write product details
            for detail in transaksi.detail_transaksi_produk:
                writer.writerow(base_data + [
                    'Produk',
                    detail.id_detailProduk,
                    detail.produk.nama_produk,
                    '-',  # No employee for products
                    detail.kuantitas,
                    float(detail.subtotal)
                ])
        
        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=transaksi_export.csv"}
        )
    except Exception as e:
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_transaksi')) 