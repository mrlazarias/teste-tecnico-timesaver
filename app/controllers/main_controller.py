from flask import Blueprint, render_template, redirect, url_for
from app.models.appointment import Appointment
from datetime import datetime, timedelta
from sqlalchemy import inspect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Verificar se as colunas existem no banco de dados
    today = datetime.now().date()
    
    try:
        # Tenta obter os próximos agendamentos
        upcoming_appointments = Appointment.query.filter(
            Appointment.date >= today
        ).order_by(Appointment.date, Appointment.time).limit(5).all()
        
        # Calcular estatísticas
        total_appointments = Appointment.query.count()
        today_appointments = Appointment.query.filter(Appointment.date == today).count()
        
        # Agendamentos da semana
        week_start = today
        week_end = today + timedelta(days=6)
        week_appointments = Appointment.query.filter(
            Appointment.date >= week_start,
            Appointment.date <= week_end
        ).count()
        
    except Exception as e:
        # Fallback para caso de erro no banco de dados
        upcoming_appointments = []
        total_appointments = 0
        today_appointments = 0
        week_appointments = 0
    
    return render_template('index.html', 
                          upcoming_appointments=upcoming_appointments,
                          total_appointments=total_appointments,
                          today_appointments=today_appointments,
                          week_appointments=week_appointments) 