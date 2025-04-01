from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.appointment import Appointment
from app import db
from datetime import datetime
from sqlalchemy import inspect

appointment_bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointment_bp.route('/', methods=['GET'])
def index():
    # Obtém parâmetros de filtro
    date_filter = request.args.get('date', '')
    client_filter = request.args.get('client', '')
    service_filter = request.args.get('service', '')
    insurance_filter = request.args.get('insurance', '')
    doctor_filter = request.args.get('doctor', '')
    status_filter = request.args.get('status', '')
    
    # Aplica os filtros
    query = Appointment.query
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(Appointment.date == filter_date)
        except ValueError:
            pass
    
    if client_filter:
        query = query.filter(Appointment.client_name.ilike(f'%{client_filter}%'))
    
    if service_filter:
        query = query.filter(Appointment.service.ilike(f'%{service_filter}%'))
    
    # Verificamos quais colunas existem no banco de dados
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('appointment')]
    
    if 'insurance' in columns and insurance_filter:
        query = query.filter(Appointment.insurance.ilike(f'%{insurance_filter}%'))
    
    if 'doctor' in columns and doctor_filter:
        query = query.filter(Appointment.doctor.ilike(f'%{doctor_filter}%'))
    
    if 'status' in columns and status_filter:
        query = query.filter(Appointment.status == status_filter)
    
    # Obtém os agendamentos com os filtros aplicados
    appointments = query.order_by(Appointment.date, Appointment.time).all()
    
    # Obtém listas de opções para os filtros de dropdown
    insurance_options = []
    doctor_options = []
    
    if 'insurance' in columns:
        insurance_options = db.session.query(Appointment.insurance).distinct().all()
    
    if 'doctor' in columns:
        doctor_options = db.session.query(Appointment.doctor).distinct().all()
    
    return render_template('appointments/index.html', 
                          appointments=appointments,
                          date_filter=date_filter,
                          client_filter=client_filter,
                          service_filter=service_filter,
                          insurance_filter=insurance_filter,
                          doctor_filter=doctor_filter,
                          status_filter=status_filter,
                          insurance_options=insurance_options,
                          doctor_options=doctor_options,
                          columns=columns)

@appointment_bp.route('/new', methods=['GET'])
def new():
    # Verificamos quais colunas existem no banco de dados
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('appointment')]
    return render_template('appointments/new.html', columns=columns)

@appointment_bp.route('/', methods=['POST'])
def create():
    try:
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time = datetime.strptime(request.form['time'], '%H:%M').time()
        
        # Crie um dicionário com os valores obrigatórios
        appointment_data = {
            'date': date,
            'time': time,
            'client_name': request.form['client_name'],
            'service': request.form['service']
        }
        
        # Verificar quais colunas existem no banco de dados
        inspector = inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('appointment')]
        
        # Adicione campos opcionais apenas se existirem no banco de dados
        if 'client_phone' in columns and request.form.get('client_phone'):
            appointment_data['client_phone'] = request.form.get('client_phone')
            
        if 'client_email' in columns and request.form.get('client_email'):
            appointment_data['client_email'] = request.form.get('client_email')
            
        if 'tuss_code' in columns and request.form.get('tuss_code'):
            appointment_data['tuss_code'] = request.form.get('tuss_code')
            
        if 'insurance' in columns and request.form.get('insurance'):
            appointment_data['insurance'] = request.form.get('insurance')
            
        if 'doctor' in columns and request.form.get('doctor'):
            appointment_data['doctor'] = request.form.get('doctor')
            
        if 'notes' in columns and request.form.get('notes'):
            appointment_data['notes'] = request.form.get('notes')
            
        if 'status' in columns and request.form.get('status'):
            appointment_data['status'] = request.form.get('status')
        
        # Crie o objeto Appointment com os dados validados
        appointment = Appointment(**appointment_data)
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Agendamento criado com sucesso!', 'success')
        return redirect(url_for('appointments.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar agendamento: {str(e)}', 'error')
        return redirect(url_for('appointments.new'))

@appointment_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    appointment = Appointment.query.get_or_404(id)
    
    # Verificamos quais colunas existem no banco de dados
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns('appointment')]
    
    return render_template('appointments/edit.html', appointment=appointment, columns=columns)

@appointment_bp.route('/<int:id>', methods=['POST'])
def update(id):
    appointment = Appointment.query.get_or_404(id)
    
    try:
        appointment.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        appointment.time = datetime.strptime(request.form['time'], '%H:%M').time()
        appointment.client_name = request.form['client_name']
        appointment.service = request.form['service']
        
        # Verificar quais colunas existem no banco de dados
        inspector = inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('appointment')]
        
        # Atualizar campos opcionais apenas se existirem no banco de dados
        if 'client_phone' in columns:
            appointment.client_phone = request.form.get('client_phone', '')
            
        if 'client_email' in columns:
            appointment.client_email = request.form.get('client_email', '')
            
        if 'tuss_code' in columns:
            appointment.tuss_code = request.form.get('tuss_code', '')
            
        if 'insurance' in columns:
            appointment.insurance = request.form.get('insurance', '')
            
        if 'doctor' in columns:
            appointment.doctor = request.form.get('doctor', '')
            
        if 'notes' in columns:
            appointment.notes = request.form.get('notes', '')
            
        if 'status' in columns:
            appointment.status = request.form.get('status', 'agendado')
        
        db.session.commit()
        
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('appointments.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar agendamento: {str(e)}', 'error')
        return redirect(url_for('appointments.edit', id=id))

@appointment_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    appointment = Appointment.query.get_or_404(id)
    
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Agendamento excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir agendamento: {str(e)}', 'error')
    
    return redirect(url_for('appointments.index')) 