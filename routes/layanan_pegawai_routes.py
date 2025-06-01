from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from models import db, LayananPegawai, Layanan, Pegawai
from decimal import Decimal
from flask_login import login_required
from flask import current_app
import csv
import io

layanan_pegawai_bp = Blueprint('layanan_pegawai', __name__)

@layanan_pegawai_bp.route('/layanan-pegawai')
@login_required
def list_layanan_pegawai():
    layanan_pegawai_list = LayananPegawai.query.all()
    return render_template('layananPegawai.html', action='list', layanan_pegawai_list=layanan_pegawai_list)

@layanan_pegawai_bp.route('/layanan-pegawai/add', methods=['GET', 'POST'])
@login_required
def add_layanan_pegawai():
    if request.method == 'POST':
        try:
            id_layanan = request.form['id_layanan']
            id_pegawai = request.form['id_pegawai']
            biaya = Decimal(request.form['biaya'])

            # Check if the combination already exists
            existing = LayananPegawai.query.filter_by(
                id_layanan=id_layanan,
                id_pegawai=id_pegawai
            ).first()

            if existing:
                flash('Pegawai sudah terdaftar untuk layanan ini', 'error')
                return redirect(url_for('layanan_pegawai.add_layanan_pegawai'))

            layanan_pegawai = LayananPegawai(
                id_layanan=id_layanan,
                id_pegawai=id_pegawai,
                biaya=biaya
            )

            db.session.add(layanan_pegawai)
            db.session.commit()
            flash('Layanan pegawai berhasil ditambahkan', 'success')
            return redirect(url_for('layanan_pegawai.list_layanan_pegawai'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('layanan_pegawai.add_layanan_pegawai'))

    layanan_list = Layanan.query.all()
    pegawai_list = Pegawai.query.all()
    return render_template('layananPegawai.html', action='add', layanan_list=layanan_list, pegawai_list=pegawai_list)

@layanan_pegawai_bp.route('/layanan-pegawai/edit/<int:id_layanan>/<int:id_pegawai>', methods=['GET', 'POST'])
@login_required
def edit_layanan_pegawai(id_layanan, id_pegawai):
    layanan_pegawai = LayananPegawai.query.filter_by(
        id_layanan=id_layanan,
        id_pegawai=id_pegawai
    ).first_or_404()

    if request.method == 'POST':
        try:
            new_id_layanan = request.form['id_layanan']
            new_id_pegawai = request.form['id_pegawai']
            biaya = Decimal(request.form['biaya'])

            # Check if the new combination already exists (excluding current record)
            existing = LayananPegawai.query.filter(
                LayananPegawai.id_layanan == new_id_layanan,
                LayananPegawai.id_pegawai == new_id_pegawai,
                ~(LayananPegawai.id_layanan == id_layanan and LayananPegawai.id_pegawai == id_pegawai)
            ).first()

            if existing:
                flash('Pegawai sudah terdaftar untuk layanan ini', 'error')
                return redirect(url_for('layanan_pegawai.edit_layanan_pegawai', id_layanan=id_layanan, id_pegawai=id_pegawai))

            layanan_pegawai.id_layanan = new_id_layanan
            layanan_pegawai.id_pegawai = new_id_pegawai
            layanan_pegawai.biaya = biaya

            db.session.commit()
            flash('Layanan pegawai berhasil diperbarui', 'success')
            return redirect(url_for('layanan_pegawai.list_layanan_pegawai'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('layanan_pegawai.edit_layanan_pegawai', id_layanan=id_layanan, id_pegawai=id_pegawai))

    layanan_list = Layanan.query.all()
    pegawai_list = Pegawai.query.all()
    return render_template('layananPegawai.html', 
                         action='edit', 
                         layanan_pegawai=layanan_pegawai,
                         layanan_list=layanan_list, 
                         pegawai_list=pegawai_list)

@layanan_pegawai_bp.route('/layanan-pegawai/delete/<int:id_layanan>/<int:id_pegawai>')
@login_required
def delete_layanan_pegawai(id_layanan, id_pegawai):
    try:
        layanan_pegawai = LayananPegawai.query.filter_by(
            id_layanan=id_layanan,
            id_pegawai=id_pegawai
        ).first_or_404()
        
        db.session.delete(layanan_pegawai)
        db.session.commit()
        flash('Layanan pegawai berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('layanan_pegawai.list_layanan_pegawai'))

@layanan_pegawai_bp.route('/layanan-pegawai/live_search')
@login_required
def live_search():
    try:
        query_param = request.args.get('q', '').strip()        
        if not query_param:
            list_layanan_pegawai = LayananPegawai.query.all()
        elif len(query_param) >= 1:
            search_pattern = f"%{query_param}%"
            list_layanan_pegawai = LayananPegawai.query.join(
                Layanan
            ).join(
                Pegawai
            ).filter(
                (Layanan.nama_layanan.ilike(search_pattern)) |
                (Pegawai.nama.ilike(search_pattern))
            ).all()
        else:
            return jsonify([])

        results = [{
            'id_layanan': lp.id_layanan,
            'id_pegawai': lp.id_pegawai,
            'nama_layanan': lp.layanan.nama_layanan,
            'nama_pegawai': lp.pegawai.nama,
            'biaya': float(lp.biaya)
        } for lp in list_layanan_pegawai]
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error in live_search: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@layanan_pegawai_bp.route('/layanan-pegawai/export_csv')
@login_required
def export_csv():
    try:
        all_data = LayananPegawai.query.all()

        if not all_data:
            flash('Tidak ada data yang dapat di export.', 'info')
            return redirect(url_for('.list_layanan_pegawai'))
        
        output = io.StringIO()
        writer = csv.writer(output)
        headers = ['id_layanan', 'nama_layanan', 'id_pegawai', 'nama_pegawai', 'biaya']
        writer.writerow(headers)

        for lp in all_data:
            row = [
                lp.id_layanan,
                lp.layanan.nama_layanan,
                lp.id_pegawai,
                lp.pegawai.nama,
                float(lp.biaya)
            ]
            writer.writerow(row)
        
        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=layanan_pegawai_export.csv"}
        )
    except Exception as e:
        current_app.logger.error(f"Error exporting Layanan Pegawai to CSV: {str(e)}")
        flash(f'Terjadi error saat membuat file CSV: {str(e)}', 'danger')
        return redirect(url_for('.list_layanan_pegawai')) 