from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from models import Produk
from database import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from flask import current_app
import csv
import io

produk_bp = Blueprint('produk', __name__)

@produk_bp.route('/produk')
@login_required
def list_produk():
    try:
        produk_list = Produk.query.all()
        return render_template('produk.html', action='list', produk_list=produk_list)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('produk.list_produk'))

@produk_bp.route('/produk/add', methods=['GET', 'POST'])
@login_required
def add_produk():
    if request.method == 'POST':
        try:
            # Validate required fields
            if not request.form.get('nama_produk'):
                raise ValueError("Nama produk harus diisi")
            
            # Validate nama_produk length
            nama_produk = request.form['nama_produk']
            if len(nama_produk) > 100:
                raise ValueError("Nama produk tidak boleh lebih dari 100 karakter")
            
            # Check if produk with same name exists
            existing_produk = Produk.query.filter_by(nama_produk=nama_produk).first()
            if existing_produk:
                raise ValueError("Produk dengan nama tersebut sudah ada")
            
            # Validate and convert numeric fields
            try:
                harga = float(request.form.get('harga', 0))
                if harga < 0:
                    raise ValueError("Harga tidak boleh negatif")
                if harga > 999999999.99:
                    raise ValueError("Harga terlalu besar")
            except ValueError:
                raise ValueError("Format harga tidak valid")
            
            try:
                stok = int(request.form.get('stok', 0))
                if stok < 0:
                    raise ValueError("Stok tidak boleh negatif")
                if stok > 999999:
                    raise ValueError("Stok terlalu besar")
            except ValueError:
                raise ValueError("Format stok tidak valid")

            produk = Produk(
                nama_produk=nama_produk,
                harga=harga,
                stok=stok
            )
            db.session.add(produk)
            db.session.commit()
            flash('Data produk berhasil ditambahkan!', 'success')
            return redirect(url_for('produk.list_produk'))
        except ValueError as ve:
            db.session.rollback()
            flash(f'Error validasi: {str(ve)}', 'error')
        except IntegrityError as ie:
            db.session.rollback()
            flash('Error: Terjadi kesalahan integritas data', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('produk.add_produk'))
    
    return render_template('produk.html', action='add')

@produk_bp.route('/produk/edit/<int:id_produk>', methods=['GET', 'POST'])
@login_required
def edit_produk(id_produk):
    try:
        produk = Produk.query.get_or_404(id_produk)
        
        if request.method == 'POST':
            try:
                # Validate required fields
                if not request.form.get('nama_produk'):
                    raise ValueError("Nama produk harus diisi")
                
                # Validate nama_produk length
                nama_produk = request.form['nama_produk']
                if len(nama_produk) > 100:
                    raise ValueError("Nama produk tidak boleh lebih dari 100 karakter")
                
                # Check if produk with same name exists (excluding current produk)
                existing_produk = Produk.query.filter(
                    Produk.nama_produk == nama_produk,
                    Produk.id_produk != id_produk
                ).first()
                if existing_produk:
                    raise ValueError("Produk dengan nama tersebut sudah ada")
                
                # Validate and convert numeric fields
                try:
                    harga = float(request.form.get('harga', 0))
                    if harga < 0:
                        raise ValueError("Harga tidak boleh negatif")
                    if harga > 999999999.99:
                        raise ValueError("Harga terlalu besar")
                except ValueError:
                    raise ValueError("Format harga tidak valid")
                
                try:
                    stok = int(request.form.get('stok', 0))
                    if stok < 0:
                        raise ValueError("Stok tidak boleh negatif")
                    if stok > 999999:
                        raise ValueError("Stok terlalu besar")
                except ValueError:
                    raise ValueError("Format stok tidak valid")

                # update detail data
                produk.nama_produk = nama_produk
                produk.harga = harga
                produk.stok = stok
                
                db.session.commit()
                flash('Data produk berhasil diperbarui!', 'success')
                return redirect(url_for('produk.list_produk'))
            except ValueError as ve:
                db.session.rollback()
                flash(f'Error validasi: {str(ve)}', 'error')
            except IntegrityError as ie:
                db.session.rollback()
                flash('Error: Terjadi kesalahan integritas data', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('produk.edit_produk', id_produk=id_produk))
        
        return render_template('produk.html', produk=produk, action='edit')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('produk.list_produk'))

@produk_bp.route('/produk/delete/<int:id_produk>', methods=['POST'])
@login_required
def delete_produk(id_produk):
    try:
        produk = Produk.query.get_or_404(id_produk)
        
        # Check for existing relationships
        if produk.detail_transaksi_produk:
            raise ValueError("Produk tidak dapat dihapus karena masih memiliki relasi dengan transaksi")
        
        db.session.delete(produk)
        db.session.commit()
        flash('Data produk berhasil dihapus!', 'success')
    except ValueError as ve:
        db.session.rollback()
        flash(f'Error validasi: {str(ve)}', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('produk.list_produk'))

@produk_bp.route('/produk/live_search')
@login_required
def live_search():
    try:
        query_param = request.args.get('q', '').strip()        
        if not query_param:
            list_produk = Produk.query.all()
        elif len(query_param) >= 1:
            search_pattern = f"%{query_param}%"
            list_produk = Produk.query.filter(
                Produk.nama_produk.ilike(search_pattern)
            ).all()
        else:
            return jsonify([])

        results = [{
            'id_produk': produk.id_produk,
            'nama_produk': produk.nama_produk,
            'harga': float(produk.harga),
            'stok': produk.stok
        } for produk in list_produk]
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error in live_search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@produk_bp.route('/produk/export_csv')
@login_required
def export_csv():
    try:
        all_data = Produk.query.all()

        if not all_data:
            flash('Tidak ada data yang dapat di export.', 'info')
            return redirect(url_for('.list_produk'))
        
        output = io.StringIO()
        writer = csv.writer(output)
        headers = ['id_produk', 'nama_produk', 'harga', 'stok']
        writer.writerow(headers)

        for produk in all_data:
            row = [
                produk.id_produk,
                produk.nama_produk,
                float(produk.harga),
                produk.stok
            ]
            writer.writerow(row)
        
        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=produk_export.csv"}
        )
    except Exception as e:
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_produk')) 