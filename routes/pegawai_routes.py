from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from models import db, Pegawai
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_login import login_required
from flask import current_app
import csv
import io
pegawai_bp = Blueprint('pegawai', __name__)

@pegawai_bp.route('/pegawai')
@login_required
def list_pegawai():
    pegawai_list = Pegawai.query.all()
    return render_template('pegawai.html', action='list', pegawai_list=pegawai_list)

@pegawai_bp.route('/pegawai/add', methods=['GET', 'POST'])
@login_required
def add_pegawai():
    if request.method == 'POST':
        nama = request.form['nama']
        no_hp = request.form['no_hp']
        jabatan = request.form['jabatan']
        gender = request.form['gender'] == 'true'  # Convert string 'true'/'false' to boolean
        
        # Check if pegawai with same name already exists
        existing_pegawai = Pegawai.query.filter_by(nama=nama).first()
        if existing_pegawai:
            flash('Pegawai dengan nama tersebut sudah ada!', 'danger')
            return render_template('pegawai.html', action='add')
        
        new_pegawai = Pegawai(
            nama=nama,
            no_hp=no_hp,
            jabatan=jabatan,
            gender=gender
        )
        
        try:
            db.session.add(new_pegawai)
            db.session.commit()
            flash('Pegawai berhasil ditambahkan!', 'success')
            return redirect(url_for('pegawai.list_pegawai'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return render_template('pegawai.html', action='add')
    
    return render_template('pegawai.html', action='add')

@pegawai_bp.route('/pegawai/edit/<int:id_pegawai>', methods=['GET', 'POST'])
@login_required
def edit_pegawai(id_pegawai):
    pegawai = Pegawai.query.get_or_404(id_pegawai)
    
    if request.method == 'POST':
        nama = request.form['nama']
        no_hp = request.form['no_hp']
        jabatan = request.form['jabatan']
        gender = request.form['gender'] == 'true'  # Convert string 'true'/'false' to boolean
        
        # Check if another pegawai with same name exists
        existing_pegawai = Pegawai.query.filter(
            Pegawai.nama == nama,
            Pegawai.id_pegawai != id_pegawai
        ).first()
        
        if existing_pegawai:
            flash('Pegawai dengan nama tersebut sudah ada!', 'danger')
            return render_template('pegawai.html', action='edit', pegawai=pegawai)
        
        try:
            pegawai.nama = nama
            pegawai.no_hp = no_hp
            pegawai.jabatan = jabatan
            pegawai.gender = gender
            pegawai.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Pegawai berhasil diupdate!', 'success')
            return redirect(url_for('pegawai.list_pegawai'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return render_template('pegawai.html', action='edit', pegawai=pegawai)
    
    return render_template('pegawai.html', action='edit', pegawai=pegawai)

@pegawai_bp.route('/pegawai/delete/<int:id_pegawai>', methods=['POST'])
@login_required
def delete_pegawai(id_pegawai):
    pegawai = Pegawai.query.get_or_404(id_pegawai)
    try:
        db.session.delete(pegawai)
        db.session.commit()
        flash('Pegawai berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    return redirect(url_for('pegawai.list_pegawai'))

@pegawai_bp.route('/pegawai/live_search')
@login_required
def live_search():
    try:
        query_param = request.args.get('q', '').strip()        
        if not query_param:
            list_pegawai = Pegawai.query.all()
        elif len(query_param) >= 1:
            search_pattern = f"%{query_param}%"
            list_pegawai = Pegawai.query.filter(
                Pegawai.nama.ilike(search_pattern)
            ).all()
        else:
            return jsonify([])

        results = [{
            'id_pegawai': pegawai.id_pegawai,
            'nama': pegawai.nama,
            'no_hp': pegawai.no_hp,
            'jabatan': pegawai.jabatan,
            'gender': 'Perempuan' if pegawai.gender else 'Laki-laki'
        } for pegawai in list_pegawai]
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error in live_search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@pegawai_bp.route('/pegawai/export_csv')
@login_required
def export_csv():
    try:
        all_data = Pegawai.query.all()

        if not all_data:
            flash('Tidak ada data yang dapat di export.', 'info')
            return redirect(url_for('.list_pegawai'))
        
        output = io.StringIO()
        writer = csv.writer(output)
        headers = ['id_pegawai', 'nama', 'no_hp', 'jabatan', 'gender']
        writer.writerow(headers)

        for pegawai in all_data:
            row = [
                pegawai.id_pegawai,
                pegawai.nama,
                pegawai.no_hp,
                pegawai.jabatan,
                'Perempuan' if pegawai.gender else 'Laki-laki'
            ]
            writer.writerow(row)
        
        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=pegawai_export.csv"}
        )
    except Exception as e:
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_pegawai')) 