from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_login import login_required
from models import KategoriLayanan
from database import db
from flask import current_app
from sqlalchemy.exc import IntegrityError
import csv
import io

kategori_bp = Blueprint('kategori', __name__)

@kategori_bp.route('/kategori', methods=['GET', 'POST'])
@login_required
def list_kategori():
    kategori_list = KategoriLayanan.query.all()
    error = None
    
    if request.method == 'POST':
        try:
            # Validate required fields
            if not request.form.get('nama_kategori'):
                raise ValueError("Nama kategori harus diisi")
            
            # Validate nama_kategori length
            nama_kategori = request.form['nama_kategori']
            if len(nama_kategori) > 100:
                raise ValueError("Nama kategori tidak boleh lebih dari 100 karakter")
            
            # Check if kategori with same name exists
            existing_kategori = KategoriLayanan.query.filter_by(nama_kategori=nama_kategori).first()
            if existing_kategori:
                raise ValueError("Kategori dengan nama tersebut sudah ada")

            kategori = KategoriLayanan(
                nama_kategori=nama_kategori
            )
            db.session.add(kategori)
            db.session.commit()
            flash('Data kategori berhasil ditambahkan!', 'success')
            return redirect(url_for('kategori.list_kategori'))
        except ValueError as ve:
            db.session.rollback()
            error = str(ve)
        except IntegrityError as ie:
            db.session.rollback()
            error = "Terjadi kesalahan integritas data"
        except Exception as e:
            db.session.rollback()
            error = str(e)
    
    return render_template('kategoriLayanan.html', kategori_list=kategori_list, error=error)

@kategori_bp.route('/kategori/edit/<int:id_kategori>', methods=['GET', 'POST'])
@login_required
def edit_kategori(id_kategori):
    kategori = KategoriLayanan.query.get_or_404(id_kategori)
    
    if request.method == 'POST':
        try:
            # Validate required fields
            if not request.form.get('nama_kategori'):
                raise ValueError("Nama kategori harus diisi")
            
            # Validate nama_kategori length
            nama_kategori = request.form['nama_kategori']
            if len(nama_kategori) > 100:
                raise ValueError("Nama kategori tidak boleh lebih dari 100 karakter")
            
            # Check if kategori with same name exists (excluding current kategori)
            existing_kategori = KategoriLayanan.query.filter(
                KategoriLayanan.nama_kategori == nama_kategori,
                KategoriLayanan.id_kategori != id_kategori
            ).first()
            if existing_kategori:
                raise ValueError("Kategori dengan nama tersebut sudah ada")

            kategori.nama_kategori = nama_kategori
            
            db.session.commit()
            flash('Data kategori berhasil diperbarui!', 'success')
            return redirect(url_for('kategori.list_kategori'))
        except ValueError as ve:
            db.session.rollback()
            flash(f'Error validasi: {str(ve)}', 'error')
        except IntegrityError as ie:
            db.session.rollback()
            flash('Error: Terjadi kesalahan integritas data', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('kategori.edit_kategori', id_kategori=id_kategori))
    
    return render_template('kategoriLayanan.html', kategori=kategori, action='edit')

@kategori_bp.route('/kategori/add', methods=['GET', 'POST'])
@login_required
def add_kategori():
    if request.method == 'POST':
        nama_kategori = request.form['nama_kategori']
        if not nama_kategori:
            flash('Nama kategori harus diisi', 'error')
            return redirect(url_for('kategori.add_kategori'))
        
        kategori = KategoriLayanan(nama_kategori=nama_kategori)
        db.session.add(kategori)
        db.session.commit()
        flash('Kategori berhasil ditambahkan', 'success')
        return redirect(url_for('kategori.list_kategori'))
    return render_template('kategoriLayanan.html', action='add')

@kategori_bp.route('/kategori/delete/<int:id_kategori>', methods=['POST'])
@login_required
def delete_kategori(id_kategori):
    kategori = KategoriLayanan.query.get_or_404(id_kategori)
    try:
        # Check for existing relationships
        if kategori.layanan:
            raise ValueError("Kategori tidak dapat dihapus karena masih memiliki layanan")
        
        db.session.delete(kategori)
        db.session.commit()
        flash('Data kategori berhasil dihapus!', 'success')
    except ValueError as ve:
        db.session.rollback()
        flash(f'Error validasi: {str(ve)}', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('kategori.list_kategori')) 

@kategori_bp.route('/kategori/live_search')
@login_required
def live_search():
    try:
        query_param = request.args.get('q', '').strip()        
        if not query_param:
            list_kategori = KategoriLayanan.query.all()
        elif len(query_param) >= 1:
            search_pattern = f"%{query_param}%"
            list_kategori = KategoriLayanan.query.filter(
                KategoriLayanan.nama_kategori.ilike(search_pattern)
            ).all()
        else:
            return jsonify([])

        results = [{
            'id_kategori': kategori.id_kategori,
            'nama_kategori': kategori.nama_kategori
        } for kategori in list_kategori]
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error in live_search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
@kategori_bp.route('/kategori/export_csv')
@login_required
def export_csv():
    try :
        all_data = KategoriLayanan.query.all()

        if not all_data:
            flash('Tidak ada data yang dapat di export.', 'info')
            return redirect(url_for('.list_kategori'))
        
        output = io.StringIO()
        writer = csv.writer(output)
        headers = ['id_kategori','nama_kategori']
        writer.writerow(headers)

        for kategori in all_data:
            row = [
                kategori.id_kategori,
                kategori.nama_kategori
            ]
            writer.writerow(row)
        
        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=kategori_layanan_export.csv"}
        )
    except Exception as e:
        current_app.logger.error(f"Error exporting Kategori Layanan to CSV: {str(e)}")
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_kategori'))