# TimeSaver - Sistema de Gestão para Clínicas

<div align="center">
  <img src="app/static/img/logotimesaver.png" alt="TimeSaver Logo" width="200">
  <h3>O futuro da saúde está aqui!</h3>
</div>

## 📋 Sobre

O TimeSaver é uma solução avançada para gestão de clínicas médicas, focada em otimizar o processo de check-in e agendamento de consultas. Com uma interface moderna e intuitiva, o sistema oferece uma experiência fluida tanto para a equipe administrativa quanto para os pacientes.

## ✨ Funcionalidades

- 📅 Gestão completa de agendamentos
- 👥 Cadastro e gestão de pacientes
- 🏥 Suporte a múltiplos convênios
- 📊 Dashboard com métricas importantes
- 📱 Interface responsiva
- 🔍 Filtros avançados de busca
- 📝 Sistema de observações e notas
- 🎯 Status de agendamentos personalizáveis

## 🚀 Tecnologias

- Python 3.8+
- Flask
- SQLAlchemy
- SQLite
- TailwindCSS
- Font Awesome

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/timesaver.git
cd timesaver
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No macOS/Linux
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
```bash
python -c "from app import db, create_app; app = create_app(); app.app_context().push(); db.create_all()"
```

5. Execute a aplicação:
```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`

## 🔧 Configuração

O sistema pode ser configurado para incluir campos adicionais no agendamento. Para isso, você tem duas opções:

### Opção 1: Usar o banco de dados existente
O sistema detectará automaticamente as colunas existentes e ajustará a interface de acordo.

### Opção 2: Criar um novo banco de dados com todos os campos
1. Exclua o arquivo `instance/scheduler.db` (se existir)
2. Execute o comando de configuração do banco de dados (passo 4 da instalação)



<div align="center">
  Feito com ❤️ pela equipe TimeSaver
</div>
