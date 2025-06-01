# Clinic Management System

A Flask-based clinic management system with MS SQL Server database.

## Prerequisites

1. Python 3.8 or higher
2. **ODBC Driver 18 for SQL Server**
   - Download from Microsoft: [https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Make sure to install the version corresponding to your operating system (x64 or x86).
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
venv\\Scripts\\activate
# For Linux/Mac:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Database Connection
The application is already configured to connect to the existing database:
- Server: RIFQI\\MSSQLSERVER01
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

## Verifying Database Connection (Optional)

If you encounter database connection issues, you can use the ODBC Data Source Administrator tool to verify that the ODBC Driver is installed and can connect to the database server:

1.  **Open ODBC Data Source Administrator**:
    - Press `Windows key + R`, type `odbcad32.exe`, and press Enter.
2.  **Go to the Drivers tab**:
    - Check if "ODBC Driver 18 for SQL Server" (or the version you installed) is listed.
3.  **Go to the System DSN or User DSN tab**:
    - Click "Add..." to set up a test connection.
    - Select the "ODBC Driver 18 for SQL Server" and click "Finish".
4.  **Configure the Test Data Source**:
    - **Name**: Enter a name (e.g., `MyFlaskDB`).
    - **Server**: Enter `RIFQI\\MSSQLSERVER01`.
    - Click "Next".
5.  **Choose Authentication**:
    - Select "With SQL Server authentication using a login ID and password entered by the user."
    - Enter "Login ID": `flaskuser`
    - Enter "Password": `database_191025`
    - Click "Next".
6.  **Configure Encryption and Trust Server Certificate**:
    - On the "Connect to SQL Server" screen, ensure **"Encrypt"** is set to **"Yes"**.
    - On the next screen (where you change the default database), check the box for **"Trust server certificate"**.
    - Click "Next" on subsequent screens.
7.  **Test the Data Source**:
    - Click "Finish".
    - In the summary window, click **"Test Data Source..."**.
    - A "TESTS COMPLETED SUCCESSFULLY!" message indicates a successful connection from your machine using the driver and credentials.

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

1.  **Database Connection Error**
    - Make sure SQL Server is running on the server (`RIFQI\\MSSQLSERVER01`).
    - Ensure **ODBC Driver 18 for SQL Server** is installed on your machine.
    - Verify your connection setup by following the steps in the "Verifying Database Connection (Optional)" section above. **Make sure to check "Trust server certificate" if you encounter SSL errors.** If the test fails there, the issue is with the driver or server connection, not the Python code.
    - Check if you can connect to the server using SSMS with the provided credentials (`flaskuser`/`database_191025`).
    - Verify network connectivity to the database server (e.g., can you ping the server machine).

2.  **Module Not Found Error**
    - Make sure virtual environment is activated.
    - Run `pip install -r requirements.txt` again.

3.  **Port Already in Use**
    - Change the port in `app.py`.
    - Or close the application using the port.

## Security Notes
- Change the default admin password after first login.
- Keep your database credentials secure.
- Regularly update dependencies for security patches.

## Support
If you encounter any issues:
1.  Check the troubleshooting section.
2.  Verify all prerequisites are installed (including the ODBC driver).
3.  Ensure you can connect to the database server using the methods described.
4.  Contact the system administrator for database access if needed. 