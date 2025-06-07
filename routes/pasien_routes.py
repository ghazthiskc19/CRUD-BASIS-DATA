from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, jsonify
from models import Pasien
from database import db
from datetime import datetime
from flask_login import login_required
import csv
import io
from sqlalchemy import or_

pasien_bp = Blueprint('pasien', __name__)

@pasien_bp.route('/pasien')
@login_required
def list_pasien():
    pasien_list = Pasien.query.all()
    return render_template('pasien.html', action='list', pasien_list=pasien_list)

@pasien_bp.route('/pasien/add', methods=['GET', 'POST'])
@login_required
def add_pasien():
    if request.method == 'POST':
        try:
            tgl_lahir = datetime.strptime(request.form['tgl_lahir'], '%Y-%m-%d').date()
            pasien = Pasien(
                nama=request.form['nama'],
                no_hp=request.form['no_hp'],
                alamat=request.form['alamat'],
                tgl_lahir=tgl_lahir,
                gender=request.form['gender'] == 'true'  
            )
            db.session.add(pasien)
            db.session.commit()
            flash('Data pasien berhasil ditambahkan!', 'success')
            return redirect(url_for('pasien.list_pasien'))
        except ValueError as ve:
            db.session.rollback()
            flash(f'Error: Format tanggal tidak valid', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('pasien.add_pasien'))
    
    return render_template('pasien.html', action='add')

@pasien_bp.route('/pasien/edit/<int:id_pasien>', methods=['GET', 'POST'])
@login_required
def edit_pasien(id_pasien):
    pasien = Pasien.query.get_or_404(id_pasien)
    
    if request.method == 'POST':
        try:
            tgl_lahir = datetime.strptime(request.form['tgl_lahir'], '%Y-%m-%d').date()
            pasien.nama = request.form['nama']
            pasien.no_hp = request.form['no_hp']
            pasien.alamat = request.form['alamat']
            pasien.tgl_lahir = tgl_lahir
            pasien.gender = request.form['gender'] == 'true'  # Convert string 'true'/'false' to boolean
            
            db.session.commit()
            flash('Data pasien berhasil diperbarui!', 'success')
            return redirect(url_for('pasien.list_pasien'))
        except ValueError as ve:
            db.session.rollback()
            flash(f'Error: Format tanggal tidak valid', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('pasien.edit_pasien', id_pasien=id_pasien))
    
    return render_template('pasien.html', pasien=pasien, action='edit')

@pasien_bp.route('/pasien/delete/<int:id_pasien>', methods=['POST'])
@login_required
def delete_pasien(id_pasien):
    pasien = Pasien.query.get_or_404(id_pasien)
    try:
        db.session.delete(pasien)
        db.session.commit()
        flash('Data pasien berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('pasien.list_pasien'))

@pasien_bp.route('/pasien/export_csv')
@login_required
def export_csv():
    try:
        all_data = Pasien.query.all()

        if not all_data:
            flash('Tidak ada data yang dapat di export.', 'info')
            return redirect(url_for('.list_pasien'))
        
        output = io.StringIO()
        writer = csv.writer(output)
        headers = ['id_pasien', 'nama', 'no_hp', 'alamat', 'tgl_lahir', 'gender']
        writer.writerow(headers)

        for pasien in all_data:
            row = [
                pasien.id_pasien,
                pasien.nama,
                pasien.no_hp,
                pasien.alamat,
                pasien.tgl_lahir.strftime('%Y-%m-%d'),
                'Perempuan' if pasien.gender else 'Laki-laki'
            ]
            writer.writerow(row)
        
        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=pasien_export.csv"}
        )
    except Exception as e:
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_pasien'))

@pasien_bp.route('/live-search')
def live_search():
    query = request.args.get('q', '')
    if len(query) < 2:
        results = Pasien.query.all()
        return jsonify([{
            'id_pasien': p.id_pasien,
            'nama': p.nama,
            'no_hp': p.no_hp,
            'alamat': p.alamat,
            'tgl_lahir': p.tgl_lahir.strftime('%Y-%m-%d') if p.tgl_lahir else '',
            'gender': 'Perempuan' if p.gender else 'Laki-laki'
        } for p in results])
    
    results = Pasien.query.filter(
        or_(
            Pasien.nama.ilike(f'%{query}%'),
            Pasien.alamat.ilike(f'%{query}%')
        )
    ).all()
    
    return jsonify([{
        'id_pasien': p.id_pasien,
        'nama': p.nama,
        'no_hp': p.no_hp,
        'alamat': p.alamat,
        'tgl_lahir': p.tgl_lahir.strftime('%Y-%m-%d') if p.tgl_lahir else '',
        'gender': 'Perempuan' if p.gender else 'Laki-laki'
    } for p in results]) 