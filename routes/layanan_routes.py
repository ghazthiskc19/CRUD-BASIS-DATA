from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_login import login_required
from models import Layanan, KategoriLayanan
from database import db
from sqlalchemy.exc import IntegrityError
from flask import current_app
import csv
import io

layanan_bp = Blueprint('layanan', __name__)

@layanan_bp.route('/layanan')
@login_required
def list_layanan():
    try:
        layanan_list = Layanan.query.all()
        return render_template('layanan.html', layanan_list=layanan_list)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('layanan.list_layanan'))

@layanan_bp.route('/layanan/add', methods=['GET', 'POST'])
@login_required
def add_layanan():
    if request.method == 'POST':
        try:
            # Validate required fields
            if not request.form.get('nama_layanan'):
                raise ValueError("Nama layanan harus diisi")
            
            if not request.form.get('id_kategori'):
                raise ValueError("Kategori layanan harus dipilih")
            
            # Validate nama_layanan length
            nama_layanan = request.form['nama_layanan']
            if len(nama_layanan) > 100:
                raise ValueError("Nama layanan tidak boleh lebih dari 100 karakter")
            
            # Check if layanan with same name exists
            existing_layanan = Layanan.query.filter_by(nama_layanan=nama_layanan).first()
            if existing_layanan:
                raise ValueError("Layanan dengan nama tersebut sudah ada")

            # Validate kategori exists
            kategori = KategoriLayanan.query.get(request.form['id_kategori'])
            if not kategori:
                raise ValueError("Kategori layanan tidak ditemukan")

            layanan = Layanan(
                nama_layanan=nama_layanan,
                id_kategori=request.form['id_kategori']
            )
            db.session.add(layanan)
            db.session.commit()
            flash('Data layanan berhasil ditambahkan!', 'success')
            return redirect(url_for('layanan.list_layanan'))
        except ValueError as ve:
            db.session.rollback()
            flash(f'Error validasi: {str(ve)}', 'error')
        except IntegrityError as ie:
            db.session.rollback()
            flash('Error: Terjadi kesalahan integritas data', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('layanan.add_layanan'))
    
    try:
        kategori_list = KategoriLayanan.query.all()
        if not kategori_list:
            flash('Peringatan: Belum ada kategori layanan. Silakan tambahkan kategori terlebih dahulu.', 'warning')
        return render_template('layanan.html', action='add', kategori_list=kategori_list)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('layanan.list_layanan'))

@layanan_bp.route('/layanan/edit/<int:id_layanan>', methods=['GET', 'POST'])
@login_required
def edit_layanan(id_layanan):
    try:
        layanan = Layanan.query.get_or_404(id_layanan)
        
        if request.method == 'POST':
            try:
                # Validate required fields
                if not request.form.get('nama_layanan'):
                    raise ValueError("Nama layanan harus diisi")
                
                if not request.form.get('id_kategori'):
                    raise ValueError("Kategori layanan harus dipilih")
                
                # Validate nama_layanan length
                nama_layanan = request.form['nama_layanan']
                if len(nama_layanan) > 100:
                    raise ValueError("Nama layanan tidak boleh lebih dari 100 karakter")
                
                # Check if layanan with same name exists (excluding current layanan)
                existing_layanan = Layanan.query.filter(
                    Layanan.nama_layanan == nama_layanan,
                    Layanan.id_layanan != id_layanan
                ).first()
                if existing_layanan:
                    raise ValueError("Layanan dengan nama tersebut sudah ada")

                # Validate kategori exists
                kategori = KategoriLayanan.query.get(request.form['id_kategori'])
                if not kategori:
                    raise ValueError("Kategori layanan tidak ditemukan")

                layanan.nama_layanan = nama_layanan
                layanan.id_kategori = request.form['id_kategori']
                
                db.session.commit()
                flash('Data layanan berhasil diperbarui!', 'success')
                return redirect(url_for('layanan.list_layanan'))
            except ValueError as ve:
                db.session.rollback()
                flash(f'Error validasi: {str(ve)}', 'error')
            except IntegrityError as ie:
                db.session.rollback()
                flash('Error: Terjadi kesalahan integritas data', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('layanan.edit_layanan', id_layanan=id_layanan))
        
        kategori_list = KategoriLayanan.query.all()
        return render_template('layanan.html', layanan=layanan, action='edit', kategori_list=kategori_list)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('layanan.list_layanan'))

@layanan_bp.route('/layanan/delete/<int:id_layanan>', methods=['POST'])
@login_required
def delete_layanan(id_layanan):
    try:
        layanan = Layanan.query.get_or_404(id_layanan)
        
        # Check for existing relationships
        if layanan.layanan_pegawai or layanan.detail_transaksi_layanan or layanan.detail_transaksi_produk:
            raise ValueError("Layanan tidak dapat dihapus karena masih memiliki relasi dengan pegawai atau transaksi")
        
        db.session.delete(layanan)
        db.session.commit()
        flash('Data layanan berhasil dihapus!', 'success')
    except ValueError as ve:
        db.session.rollback()
        flash(f'Error validasi: {str(ve)}', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('layanan.list_layanan'))

@layanan_bp.route('/layanan/live_search')
@login_required
def live_search():
    try:
        query_param = request.args.get('q', '').strip()        
        if not query_param:
            list_layanan = Layanan.query.all()
        elif len(query_param) >= 1:
            search_pattern = f"%{query_param}%"
            list_layanan = Layanan.query.filter(
                Layanan.nama_layanan.ilike(search_pattern)
            ).all()
        else:
            return jsonify([])

        results = [{
            'id_layanan': layanan.id_layanan,
            'nama_layanan': layanan.nama_layanan,
            'kategori': layanan.kategori.nama_kategori if layanan.kategori else None
        } for layanan in list_layanan]
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error in live_search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@layanan_bp.route('/layanan/export_csv')
@login_required
def export_csv():
    try:
        all_data = Layanan.query.all()

        if not all_data:
            flash('Tidak ada data yang dapat di export.', 'info')
            return redirect(url_for('.list_layanan'))
        
        output = io.StringIO()
        writer = csv.writer(output)
        headers = ['id_layanan', 'nama_layanan', 'kategori']
        writer.writerow(headers)

        for layanan in all_data:
            row = [
                layanan.id_layanan,
                layanan.nama_layanan,
                layanan.kategori.nama_kategori if layanan.kategori else '-'
            ]
            writer.writerow(row)
        
        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=layanan_export.csv"}
        )
    except Exception as e:
        current_app.logger.error(f"Error exporting Layanan to CSV: {str(e)}")
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_layanan')) 