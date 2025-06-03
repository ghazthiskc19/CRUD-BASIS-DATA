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
                
                if not layanan_ids or not all(layanan_ids):
                    raise ValueError("Transaksi harus memiliki minimal satu layanan yang dipilih")
                
                for i in range(len(layanan_ids)):
                    if not layanan_ids[i] or not pegawai_ids[i] or not kuantitas_layanan[i]:
                        raise ValueError("Semua field layanan harus diisi untuk setiap item layanan")
                    
                    try:
                        kuantitas = int(kuantitas_layanan[i])
                        if kuantitas <= 0:
                            raise ValueError("Kuantitas layanan harus lebih dari 0")
                    except ValueError:
                        raise ValueError("Format kuantitas layanan tidak valid")
                    
                    layanan = Layanan.query.get(layanan_ids[i])
                    pegawai = Pegawai.query.get(pegawai_ids[i])
                    
                    if not layanan or not pegawai:
                        raise ValueError("Layanan atau pegawai tidak ditemukan (ID tidak valid)")
                    
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
                        if produk_ids[i] and kuantitas_produk[i]:
                            try:
                                kuantitas = int(kuantitas_produk[i])
                                if kuantitas <= 0:
                                    raise ValueError("Kuantitas produk harus lebih dari 0")
                            except ValueError:
                                raise ValueError("Format kuantitas produk tidak valid")
                            
                            produk = Produk.query.get(produk_ids[i])
                            if not produk:
                                raise ValueError(f"Produk dengan ID {produk_ids[i]} tidak ditemukan")
                            
                            if produk.stok < kuantitas:
                                raise ValueError(f"Stok produk {produk.nama_produk} ({produk.stok}) tidak mencukupi untuk kuantitas {kuantitas}")
                            
                            subtotal = produk.harga * Decimal(str(kuantitas))
                            total_harga += subtotal
                            
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
            current_app.logger.error(f"Integrity Error during add_transaksi: {ie}")
            flash('Error: Terjadi kesalahan integritas data. Pastikan semua input benar.', 'error')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected Error during add_transaksi: {e}", exc_info=True)
            flash(f'Error: Terjadi kesalahan saat menyimpan transaksi: {str(e)}', 'error')
            
        return redirect(url_for('transaksi.add_transaksi'))
    
    pasien_list = Pasien.query.all()
    layanan_list = Layanan.query.all()
    produk_list = Produk.query.all()
    pegawai_list = Pegawai.query.all()
    
    for layanan in layanan_list:
        layanan.layanan_pegawai_data = [
            {
                'id_pegawai': lp.id_pegawai,
                'biaya': float(lp.biaya)
            }
            for lp in layanan.layanan_pegawai
        ]
    
    pegawai_data = [
        {
            'id_pegawai': p.id_pegawai,
            'nama': p.nama
        }
        for p in pegawai_list
    ]
    
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
        current_app.logger.error(f"Error during delete_transaksi {id_transaksi}: {e}", exc_info=True)
        flash(f'Error saat menghapus transaksi: {str(e)}', 'error')
    return redirect(url_for('transaksi.list_transaksi'))

@transaksi_bp.route('/transaksi/live_search')
@login_required
def live_search():
    try:
        query_param = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all')  # 'all', 'pasien', 'tanggal', 'bulan'
        
        if not query_param:
            list_transaksi = Transaksi.query.all()
        else:
            base_query = Transaksi.query.join(Pasien)
            
            if search_type == 'all':
                list_transaksi = base_query.filter(
                    (Pasien.nama.ilike(f"%{query_param}%")) |
                    (Transaksi.tanggal.cast(String).ilike(f"%{query_param}%"))
                ).all()
            elif search_type == 'pasien':
                list_transaksi = base_query.filter(
                    Pasien.nama.ilike(f"%{query_param}%")
                ).all()
            elif search_type == 'tanggal':
                try:
                    search_date = datetime.strptime(query_param, '%Y-%m-%d').date()
                    list_transaksi = base_query.filter(
                        Transaksi.tanggal == search_date
                    ).all()
                except ValueError:
                    list_transaksi = []
            elif search_type == 'bulan':
                try:
                    year, month = map(int, query_param.split('-'))
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
        current_app.logger.error(f"Error in live_search: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@transaksi_bp.route('/transaksi/export_csv')
@login_required
def export_csv():
    try:
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
        
        writer.writerow([
            'ID Transaksi', 'Tanggal', 'Nama Pasien', 'Total Harga',
            'Tipe Detail', 'ID Detail', 'Nama Item', 'Pegawai', 'Kuantitas', 'Subtotal'
        ])

        for transaksi in all_transaksi:
            base_data = [
                transaksi.id_transaksi,
                transaksi.tanggal.strftime('%Y-%m-%d'),
                transaksi.pasien.nama,
                float(transaksi.total_harga)
            ]
            
            for detail in transaksi.detail_transaksi_layanan:
                writer.writerow(base_data + [
                    'Layanan',
                    detail.id_detailLayanan,
                    detail.layanan.nama_layanan,
                    detail.pegawai.nama,
                    detail.kuantitas,
                    float(detail.subtotal)
                ])
            
            for detail in transaksi.detail_transaksi_produk:
                writer.writerow(base_data + [
                    'Produk',
                    detail.id_detailProduk,
                    detail.produk.nama_produk,
                    '-',
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
        current_app.logger.error(f"Error during export_csv: {e}", exc_info=True)
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_transaksi')) 