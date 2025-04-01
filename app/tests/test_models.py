import pytest
from datetime import date, time, datetime
from app import create_app, db
from app.models.appointment import Appointment

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    with app.app_context():
        db.create_all()
        
        # Adiciona dados de teste
        test_appointment = Appointment(
            date=date(2023, 12, 31),
            time=time(14, 30),
            client_name="Test Client",
            service="Test Service"
        )
        db.session.add(test_appointment)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_appointment_model(app):
    with app.app_context():
        # Testa criação de agendamento
        new_appointment = Appointment(
            date=date(2023, 10, 15),
            time=time(9, 0),
            client_name="John Doe",
            service="Haircut"
        )
        db.session.add(new_appointment)
        db.session.commit()
        
        saved_appointment = Appointment.query.filter_by(client_name="John Doe").first()
        assert saved_appointment is not None
        assert saved_appointment.date == date(2023, 10, 15)
        assert saved_appointment.time == time(9, 0)
        assert saved_appointment.service == "Haircut"
        
        # Testa atualização de agendamento
        saved_appointment.service = "Beard Trim"
        db.session.commit()
        
        updated_appointment = Appointment.query.filter_by(client_name="John Doe").first()
        assert updated_appointment.service == "Beard Trim"
        
        # Testa método to_dict
        appointment_dict = updated_appointment.to_dict()
        assert appointment_dict['client_name'] == "John Doe"
        assert appointment_dict['service'] == "Beard Trim"
        assert appointment_dict['date'] == "2023-10-15"
        assert appointment_dict['time'] == "09:00"
        
        # Testa exclusão de agendamento
        db.session.delete(updated_appointment)
        db.session.commit()
        
        deleted_appointment = Appointment.query.filter_by(client_name="John Doe").first()
        assert deleted_appointment is None 