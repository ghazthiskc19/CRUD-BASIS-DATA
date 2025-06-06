# Clinic Management System

A Flask-based clinic management system with MS SQL Server database.

## Prerequisites

1. Python 3.8 or higher
2. **MS SQL Server (Express Edition Recommended)**
   - Download from Microsoft: [https://www.microsoft.com/en-us/sql-server/sql-server-downloads](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
   - Choose the free **Express** edition.
3. **ODBC Driver 18 for SQL Server**
   - Download from Microsoft: [https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Make sure to install the version corresponding to your operating system (x64 or x86).
4. Git (optional, for version control)

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

### 3. Database Setup

1.  **Install SQL Server Express**:
    - Download and run the installer from the Microsoft link above.
    - Choose the **Basic** or **Custom** installation type.
    - If choosing Custom, install the Database Engine.
    - During installation, note down the **Instance Name**. A common default is `SQLEXPRESS`. If you choose a custom name, remember it.
    - Choose **Mixed Mode Authentication** when prompted, and set a strong password for the `sa` (System Administrator) account. You might also want to add your current Windows user account.
2.  **Install SQL Server Management Studio (SSMS)** (Optional but Recommended):
    - Download SSMS from Microsoft's website (link is usually provided during SQL Server Express installation or can be found separately).
    - Use SSMS to connect to your local SQL Server instance.
3.  **Create the Database**:
    - Using SSMS or another tool, connect to your local SQL Server instance.
    - You can run the `schema.sql` file to create all the necessary tables. This file contains the complete database schema with all required tables and their relationships.
    - Optionally, you can run the `dummy_data.sql` file to populate the database with sample data. This includes test users, patients, employees, services, products, and transactions.
    - To run these SQL files in SSMS:
      1. Open SSMS and connect to your SQL Server instance
      2. Open the `schema.sql` file in SSMS
      3. Click "Execute" or press F5 to run the script
      4. Repeat the same process for `dummy_data.sql` if you want to add sample data
4.  **Create a SQL Server User (Optional but Recommended)**:
    - In SSMS, expand Security -> Logins.
    - Right-click Logins and select "New Login...".
    - Choose "SQL Server authentication".
    - Set "Login name" to `flaskuser`.
    - Set "Password" to `database_191025` (or a different password).
    - Uncheck "Enforce password policy" and "Enforce password expiration" for simplicity in development (but be aware of security implications).
    - Set "Default database" to `MyFlaskDB`.
    - Go to the "User Mapping" page, check the map box for `MyFlaskDB`, and in the "Database role membership" for `MyFlaskDB`, check `db_owner`.
    - Click OK.

### 4. Configure Database Connection in `app.py`

Modify the `SQLALCHEMY_DATABASE_URI` line in `app.py` to connect to your *local* SQL Server instance using SQL Server Authentication. Replace `YOUR_SERVER_NAME\YOUR_INSTANCE_NAME` with your actual server and instance name (e.g., `YOUR_COMPUTER_NAME\SQLEXPRESS` or just `localhost\SQLEXPRESS` if connecting from the same machine). Keep the username and password as `flaskuser` and `database_191025` if you created that user.

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://flaskuser:database_191025@YOUR_SERVER_NAME\\YOUR_INSTANCE_NAME/MyFlaskDB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
```
*Replace `YOUR_SERVER_NAME\\YOUR_INSTANCE_NAME` with your local SQL Server instance name.* You might be able to use `localhost\\SQLEXPRESS` or just `localhost` if it's the default instance.

### 5. Run the Application
```bash
# Make sure your virtual environment is activated
python app.py
```

The `db.create_all()` call in `app.py` will create the necessary tables in your local `MyFlaskDB` database.

### 6. Access the Application
- Open your web browser
- Go to `http://localhost:5000`
- Login with these default credentials:
  - Username: `admin`
  - Password: `admin123`

## Verifying Database Connection (Optional)

If you encounter database connection issues after configuring your local database, you can use the ODBC Data Source Administrator tool to verify that the ODBC Driver is installed and can connect to your local database server:

1.  **Open ODBC Data Source Administrator**:
    - Press `Windows key + R`, type `odbcad32.exe`, and press Enter.
2.  **Go to the Drivers tab**:
    - Check if "ODBC Driver 18 for SQL Server" (or the version you installed) is listed.
3.  **Go to the System DSN or User DSN tab**:
    - Click "Add..." to set up a test connection.
    - Select the "ODBC Driver 18 for SQL Server" and click "Finish".
4.  **Configure the Test Data Source**:
    - **Name**: Enter a name (e.g., `MyFlaskDB_Local`).
    - **Server**: Enter your local SQL Server instance name (e.g., `localhost\\SQLEXPRESS`).
    - Click "Next".
5.  **Choose Authentication**:
    - Select "With SQL Server authentication using a login ID and password entered by the user."
    - Enter "Login ID": `flaskuser`
    - Enter "Password": `database_191025`
    - Click "Next".
6.  **Configure Encryption and Trust Server Certificate**:
    - On the "Connect to SQL Server" screen, ensure **"Encrypt"** is set to **"Yes"**.
    - On the next screen (where you change the default database), check the box for **"Trust server certificate"** (needed if your local SQL Server uses a self-signed certificate).
    - Click "Next" on subsequent screens.
7.  **Test the Data Source**:
    - Click "Finish".
    - In the summary window, click **"Test Data Source..."**.
    - A "TESTS COMPLETED SUCCESSFULLY!" message indicates a successful connection.

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
    - Ensure your local SQL Server instance is running.
    - Verify the **Instance Name** in your `app.py` connection string matches your local SQL Server instance name.
    - If using SQL Server Authentication, ensure the user (`flaskuser`) and password (`database_191025`) are correct and the user has permissions to the `MyFlaskDB` database.
    - Ensure **ODBC Driver 18 for SQL Server** is installed.
    - Use the steps in "Verifying Database Connection (Optional)" to test the connection outside of the application. **Make sure to check "Trust server certificate" if you encounter SSL errors during the test.**
    - Check Windows Firewall on your local machine (though usually less of an issue for `localhost` connections).

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
2.  Verify all prerequisites are installed (including SQL Server Express and the ODBC driver).
3.  Ensure your local database and user are set up correctly.
4.  Verify you can connect to your local database using the ODBC Administrator test. 