from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, Date, Time, String, Text, DateTime

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=True, default=None)
    client_email = db.Column(db.String(100), nullable=True, default=None)
    
    # Campos de clínica médica
    service = db.Column(db.String(100), nullable=False)
    tuss_code = db.Column(db.String(20), nullable=True, default=None)
    insurance = db.Column(db.String(100), nullable=True, default=None)
    doctor = db.Column(db.String(100), nullable=True, default=None)
    notes = db.Column(db.Text, nullable=True, default=None)
    
    status = db.Column(db.String(20), default='agendado')
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Appointment {self.id}: {self.client_name}, {self.date} {self.time}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime("%Y-%m-%d"),
            "time": self.time.strftime("%H:%M"),
            "client_name": self.client_name,
            "client_phone": self.client_phone,
            "client_email": self.client_email,
            "service": self.service,
            "tuss_code": self.tuss_code,
            "insurance": self.insurance,
            "doctor": self.doctor,
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        } 