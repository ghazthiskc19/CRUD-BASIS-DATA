# Clinic Management System

A Flask-based clinic management system with MS SQL Server database.

## Prerequisites

1. Python 3.8 or higher
2. ODBC Driver 18 for SQL Server
3. Git (optional, for version control)

## Setup Instructions

### 1. Clone or Download the Project
- Download the project files
- Extract them to a folder of your choice

### 2. Set Up Python Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For Linux/Mac:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Database Connection
The application is already configured to connect to the existing database:
- Server: RIFQI\MSSQLSERVER01
- Database: MyFlaskDB
- Username: flaskuser
- Password: database_191025

No additional database setup is required.

### 4. Run the Application
```bash
# Make sure your virtual environment is activated
python app.py
```

### 5. Access the Application
- Open your web browser
- Go to `http://localhost:5000`
- Login with these default credentials:
  - Username: `admin`
  - Password: `admin123`

## Project Structure
```
clinic-crud/
├── app.py              # Main application file
├── database.py         # Database configuration
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── routes/            # Route handlers
│   ├── __init__.py
│   ├── pasien_routes.py
│   ├── pegawai_routes.py
│   ├── layanan_routes.py
│   ├── produk_routes.py
│   ├── transaksi_routes.py
│   ├── kategori_layanan_routes.py
│   └── layanan_pegawai_routes.py
└── templates/         # HTML templates
    ├── base.html
    ├── login.html
    └── ...
```

## Features
- Patient Management
- Employee Management
- Service Management
- Product Management
- Transaction Management
- Service Category Management
- CSV Export functionality
- User Authentication

## Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Make sure SQL Server is running on the server
   - Ensure ODBC Driver 18 is installed
   - Check if you can connect to the server using SSMS

2. **Module Not Found Error**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt` again

3. **Port Already in Use**
   - Change the port in `app.py`
   - Or close the application using the port

## Security Notes
- Change the default admin password after first login
- Keep your database credentials secure
- Regularly update dependencies for security patches

## Support
If you encounter any issues:
1. Check the troubleshooting section
2. Verify all prerequisites are installed
3. Ensure you can connect to the database server
4. Contact the system administrator for database access 