# IPO Management System

A comprehensive Django-based system for managing Initial Public Offerings (IPOs) with REST API and modern Bootstrap 5 frontend.

## Features

### Core Features
- **Company Management**: Create and manage companies with logos
- **IPO Tracking**: Complete IPO lifecycle management (Upcoming → Ongoing → Listed)
- **Document Management**: Upload and manage RHP & DRHP PDFs
- **Calculated Metrics**: Automatic calculation of listing gain and current returns
- **Search & Filter**: Advanced search and filtering capabilities
- **Statistics Dashboard**: Real-time IPO statistics and analytics

### Technical Features
- **Django REST Framework**: Full CRUD API with ViewSets and routers
- **PostgreSQL Database**: Robust data storage with proper relationships
- **Bootstrap 5 Frontend**: Modern, responsive UI with interactive components
- **Media Upload**: Secure file upload for logos and documents
- **Pagination**: Efficient data handling with pagination
- **Admin Interface**: Comprehensive Django admin for data management

## Tech Stack

### Backend
- **Python 3.12.3**
- **Django 5.0.6**
- **Django REST Framework 3.15.1**
- **PostgreSQL** (Database)
- **Pillow** (Image processing)

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5** (via CDN)
- **Bootstrap Icons**

### Tools
- **Postman** (API testing)
- **Git & GitHub** (Version control)

## Installation & Setup

### Prerequisites
- Python 3.12.3 or higher
- PostgreSQL database
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ipo_projects
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install django==5.0.6 djangorestframework==3.15.1 psycopg2-binary Pillow django-filter
```

### 4. Database Setup
1. Create a PostgreSQL database:
```sql
CREATE DATABASE ipo_management_db;
CREATE USER ipo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ipo_management_db TO ipo_user;
```

2. Update database settings in `ipo_management/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ipo_management_db',
        'USER': 'ipo_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## Project Structure

```
ipo_projects/
├── ipo_management/          # Django project settings
├── ipo/                     # Main app
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # ViewSets and views
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin configuration
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Homepage
│   └── ipo_detail.html    # IPO detail page
├── static/                 # Static files
│   └── images/            # Images and logos
├── media/                  # Uploaded files
├── Bluestock Logos/        # Logo assets
└── manage.py              # Django management script
```

## API Endpoints

### Companies
- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create new company
- `GET /api/companies/{id}/` - Get company details
- `PUT /api/companies/{id}/` - Update company
- `DELETE /api/companies/{id}/` - Delete company

### IPOs
- `GET /api/ipos/` - List all IPOs (with pagination)
- `POST /api/ipos/` - Create new IPO
- `GET /api/ipos/{id}/` - Get IPO details
- `PUT /api/ipos/{id}/` - Update IPO
- `DELETE /api/ipos/{id}/` - Delete IPO
- `GET /api/ipos/statistics/` - Get IPO statistics
- `GET /api/ipos/?status=upcoming` - Filter by status
- `GET /api/ipos/?search=company` - Search by company name

### Documents
- `GET /api/documents/` - List all documents
- `POST /api/documents/` - Create new document
- `GET /api/documents/{id}/` - Get document details
- `PUT /api/documents/{id}/` - Update document
- `DELETE /api/documents/{id}/` - Delete document
- `POST /api/documents/{id}/upload_rhp/` - Upload RHP PDF
- `POST /api/documents/{id}/upload_drhp/` - Upload DRHP PDF

## Frontend Pages

### Homepage (`/`)
- IPO listing with company logos and status badges
- Real-time statistics dashboard
- Search and filter functionality
- Responsive card layout

### IPO Detail (`/ipo/{id}/`)
- Complete IPO information
- Pricing details with calculated metrics
- Document download links
- Timeline visualization
- Company information

## Database Models

### Company
- `id`: Primary key
- `name`: Company name (unique)
- `logo`: Company logo image
- `created_at`, `updated_at`: Timestamps

### IPO
- `id`: Primary key
- `company`: Foreign key to Company
- `price_band_lower`, `price_band_upper`: Price range
- `open_date`, `close_date`: IPO dates
- `issue_size`: Issue size in crores
- `issue_type`: Book building, Fixed price, or Auction
- `listing_date`: Date of listing
- `status`: Upcoming, Ongoing, or Listed
- `ipo_price`, `listing_price`, `current_market_price`: Pricing data
- Calculated properties: `listing_gain`, `current_return`

### Document
- `id`: Primary key
- `ipo`: Foreign key to IPO
- `rhp_pdf`: Red Herring Prospectus file
- `drhp_pdf`: Draft Red Herring Prospectus file
- `created_at`, `updated_at`: Timestamps

## Usage Examples

### Creating an IPO via API
```bash
curl -X POST http://localhost:8000/api/ipos/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 1,
    "price_band_lower": 100.00,
    "price_band_upper": 120.00,
    "open_date": "2024-01-15",
    "close_date": "2024-01-18",
    "issue_size": 500.00,
    "issue_type": "book_building",
    "status": "upcoming"
  }'
```

### Uploading a Document
```bash
curl -X POST http://localhost:8000/api/documents/1/upload_rhp/ \
  -F "rhp_pdf=@document.pdf"
```

## Postman Collection

Import the `IPO_Management_API.postman_collection.json` file into Postman for comprehensive API testing.

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- Manage companies, IPOs, and documents
- Upload company logos
- View calculated metrics
- Monitor system statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the GitHub repository. 

## 🔗 Live Application
https://blustock-1.onrender.com
