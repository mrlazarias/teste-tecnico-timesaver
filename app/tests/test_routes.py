import pytest
from datetime import date, time
from app import create_app, db
from app.models.appointment import Appointment

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
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

def test_index_route(client):
    # Testa página de listagem de agendamentos
    response = client.get('/appointments/')
    assert response.status_code == 200
    assert b'Appointments' in response.data
    assert b'Test Client' in response.data
    assert b'Test Service' in response.data

def test_create_appointment(client, app):
    # Testa página do formulário de novo agendamento
    response = client.get('/appointments/new')
    assert response.status_code == 200
    assert b'New Appointment' in response.data
    
    # Testa criação de agendamento
    appointment_data = {
        'date': '2023-11-15',
        'time': '10:15',
        'client_name': 'Maria Silva',
        'service': 'Manicure'
    }
    
    response = client.post('/appointments/', data=appointment_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Appointment created successfully' in response.data
    assert b'Maria Silva' in response.data
    assert b'Manicure' in response.data
    
    # Verifica no banco de dados
    with app.app_context():
        appointment = Appointment.query.filter_by(client_name='Maria Silva').first()
        assert appointment is not None
        assert appointment.service == 'Manicure'

def test_edit_appointment(client, app):
    with app.app_context():
        appointment = Appointment.query.filter_by(client_name='Test Client').first()
        appointment_id = appointment.id
    
    # Testa página do formulário de edição
    response = client.get(f'/appointments/{appointment_id}/edit')
    assert response.status_code == 200
    assert b'Edit Appointment' in response.data
    assert b'Test Client' in response.data
    
    # Testa atualização de agendamento
    updated_data = {
        'date': '2023-12-31',
        'time': '15:45',
        'client_name': 'Test Client Updated',
        'service': 'Test Service Updated'
    }
    
    response = client.post(f'/appointments/{appointment_id}', data=updated_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Appointment updated successfully' in response.data
    assert b'Test Client Updated' in response.data
    
    # Verifica no banco de dados
    with app.app_context():
        updated_appointment = Appointment.query.get(appointment_id)
        assert updated_appointment.client_name == 'Test Client Updated'
        assert updated_appointment.service == 'Test Service Updated'

def test_delete_appointment(client, app):
    with app.app_context():
        # Obtém ID do agendamento de teste
        appointment_id = Appointment.query.filter_by(client_name='Test Client').first().id
    
    # Testa exclusão de agendamento
    response = client.post(f'/appointments/{appointment_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Appointment deleted successfully' in response.data
    
    # Verifica exclusão no banco de dados
    with app.app_context():
        appointment = Appointment.query.get(appointment_id)
        assert appointment is None

def test_filter_appointments(client, app):
    with app.app_context():
        # Adiciona mais agendamentos de teste para filtragem
        appointments = [
            Appointment(
                date=date(2023, 11, 10),
                time=time(9, 0),
                client_name="Client A",
                service="Service X"
            ),
            Appointment(
                date=date(2023, 11, 10),
                time=time(10, 0),
                client_name="Client B",
                service="Service Y"
            ),
            Appointment(
                date=date(2023, 11, 11),
                time=time(11, 0),
                client_name="Client A",
                service="Service Z"
            )
        ]
        db.session.add_all(appointments)
        db.session.commit()
    
    # Testa filtro por data
    response = client.get('/appointments/?date=2023-11-10')
    assert response.status_code == 200
    assert b'Client A' in response.data
    assert b'Client B' in response.data
    assert b'Service X' in response.data
    assert b'Service Y' in response.data
    
    # Testa filtro por nome do cliente
    response = client.get('/appointments/?client=Client+A')
    assert response.status_code == 200
    assert b'Client A' in response.data
    assert b'Service X' in response.data
    assert b'Service Z' in response.data
    assert b'Client B' not in response.data
    
    # Testa filtro por serviço
    response = client.get('/appointments/?service=Service+Y')
    assert response.status_code == 200
    assert b'Client B' in response.data
    assert b'Service Y' in response.data
    assert b'Client A' not in response.data
    
    # Testa filtros combinados
    response = client.get('/appointments/?date=2023-11-10&client=Client+A')
    assert response.status_code == 200
    assert b'Client A' in response.data
    assert b'Service X' in response.data
    assert b'Client B' not in response.data
    assert b'Service Z' not in response.data 