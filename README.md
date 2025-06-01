# Beauty Clinic CRUD Application

A web-based clinic management system built with Flask that helps manage clinic operations including patient records, services, and transactions.

## Features

- Kategori Layanan Management
- Layanan Management
- Produk Management
- Pegawai Management
- Layanan Pegawai Management
- Pasien Management
- Transaksi Management
- Live Search functionality
- User Authentication

## Tech Stack

- Python 3.x
- Flask
- SQLAlchemy
- Bootstrap 5
- SQLite/PostgreSQL

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/clinic-management.git
cd clinic-management
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## Project Structure

```
clinic-management/
├── app/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
├── migrations/
├── instance/
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 