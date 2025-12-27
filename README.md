# TARS Club Website

A modern full-stack web application for club management built with Django 5.2 LTS, Django REST Framework 3.16, React 19, and PostgreSQL.

## 🚀 Tech Stack

### Backend
- **Django 5.2 LTS** - Python web framework
- **Django REST Framework 3.16** - RESTful API
- **PostgreSQL 16** - Database
- **Python 3.13** - Programming language

### Frontend
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server

### DevOps
- **Docker & Docker Compose** - Containerization
- **PostgreSQL (Docker)** - Database in container

## 📋 Prerequisites

- Python 3.13+
- Node.js 18+
- Docker & Docker Compose
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd TARS
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations (requires PostgreSQL running)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
cd frontend/app

# Install dependencies
npm install

# Run development server
npm run dev
```

### 4. Database Setup (Docker)

```bash
# Start PostgreSQL container
docker-compose up -d db

# Or start all services
docker-compose up
```

## 🐳 Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📱 Access Points

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Admin Portal:** http://localhost:8000/admin
- **Health Check:** http://localhost:8000/api/health/
- **API Info:** http://localhost:8000/api/info/

## 🔑 Default Credentials

**Admin Portal:**
- Username: `admin`
- Password: `admin`

⚠️ **Change these credentials in production!**

## 📁 Project Structure

```
TARS/
├── backend/
│   ├── tars/               # Django project settings
│   │   ├── settings.py     # Configuration
│   │   ├── urls.py         # URL routing
│   │   └── views.py        # API views
│   ├── venv/               # Python virtual environment
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container config
│   ├── .env.example        # Environment variables template
│   └── .gitignore
│
├── frontend/
│   ├── app/
│   │   ├── src/
│   │   │   ├── services/   # API services
│   │   │   ├── App.tsx     # Main component
│   │   │   └── ...
│   │   ├── package.json
│   │   └── vite.config.ts
│   ├── Dockerfile          # Frontend container config
│   └── .gitignore
│
├── docker-compose.yaml     # Multi-container setup
├── .gitignore
└── README.md
```

## 🔧 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=tars_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## 🧪 Testing the Setup

1. **Health Check API:**
```bash
curl http://localhost:8000/api/health/
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-27T07:09:26.069884+00:00",
  "service": "TARS Backend API",
  "database": "connected"
}
```

2. **Frontend Health Display:**
   - Visit http://localhost:5173
   - Should show green checkmarks for backend and database

3. **Admin Portal:**
   - Visit http://localhost:8000/admin
   - Login with admin credentials

## 📊 Database Management

### Using Docker

```bash
# Connect to PostgreSQL container
docker-compose exec db psql -U postgres -d tars_db

# Inside PostgreSQL:
\dt                           # List tables
\d auth_user                  # Describe users table
SELECT * FROM auth_user;      # View users
\q                            # Exit
```

### Using GUI Tools (pgAdmin, DBeaver)

- Host: `localhost`
- Port: `5432`
- Database: `tars_db`
- User: `postgres`
- Password: `postgres`

## 🚀 Deployment

### Azure Deployment

1. **Create Azure Resources:**
   - Azure Database for PostgreSQL
   - Azure App Service (Backend)
   - Azure Static Web Apps (Frontend)

2. **Update Environment Variables:**
   - Set production database credentials
   - Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
   - Set `DEBUG=False`

3. **Database Migration:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Team

TARS Club Development Team

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact: admin@tars.com
