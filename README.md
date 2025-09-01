# Event Niti - University Event Management System

A comprehensive Django-based web application designed to streamline event management for educational institutions. Event Niti provides a complete platform for organizing, managing, and participating in university events with features like registration, certification, badges, and more.

## 🎯 Purpose

Event Niti serves as a centralized platform for universities to:
- **Organize Events**: Create and manage various academic and extracurricular events
- **Student Engagement**: Enable students to discover, register, and participate in events
- **Digital Certification**: Issue digital certificates and badges for event participation
- **Event Analytics**: Track attendance, reviews, and event performance
- **Resource Sharing**: Provide access to previous year question papers and study materials

## 🚀 Key Features

### Event Management
- **Event Creation & Publishing**: Comprehensive event creation with posters, descriptions, and scheduling
- **Registration System**: Automated registration with capacity limits and waitlists
- **Ticket Generation**: QR code-based digital tickets for event entry
- **Attendance Tracking**: Digital attendance management for coordinators
- **Event Results**: Publish competition results with winner announcements

### User Management
- **Student Profiles**: Complete student information with course, section, and year details
- **Role-based Access**: Different access levels for students, coordinators, and administrators
- **Email Verification**: Secure account verification system
- **Password Recovery**: Forgot password functionality with email tokens

### Digital Credentials
- **Certificate Generation**: Automated digital certificate creation for event participants
- **Badge System**: Achievement badges for various accomplishments
- **Verification System**: Secure hash-based certificate verification
- **Bulk Distribution**: Mass certificate and badge distribution tools

### Content Management
- **Blog System**: Event-related blog posts and announcements
- **Memory Gallery**: Photo and video galleries for past events
- **Question Papers**: Repository of previous year examination papers
- **Resource Library**: Organized academic resources by department and course

### Interactive Features
- **Event Reviews**: Rating and review system for events
- **Live Polls**: Real-time polling during events
- **Q&A Sessions**: Interactive question-answer sessions
- **Contact System**: Inquiry and support ticket system

### Payment Integration
- **Razorpay Integration**: Secure payment processing for paid events
- **Transaction Management**: Payment tracking and receipt generation
- **Refund Handling**: Automated refund processing capabilities

## 🛠 Technology Stack

### Backend
- **Framework**: Django 5.1.5
- **Database**: MySQL with utf8mb4 charset support
- **Caching**: Redis for session management and caching
- **Task Queue**: Celery for asynchronous task processing
- **Email**: SMTP integration for notifications

### Frontend
- **Templates**: Django template engine with custom CSS
- **Rich Text**: CKEditor 5 for content creation
- **Responsive Design**: Mobile-friendly interface
- **Interactive Elements**: JavaScript for dynamic functionality

### Additional Libraries
- **PDF Generation**: PDFKit for certificate creation
- **QR Codes**: QRCode library for ticket generation
- **Image Processing**: Pillow for image handling
- **Excel Support**: OpenPyXL for data export/import
- **Security**: Cryptography for secure operations

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+
- Redis Server
- Git

## 🔧 Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd ppuu
```

### 2. Create Virtual Environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DOMAIN_NAME=http://127.0.0.1:8000/
ALLOWED_HOSTS=127.0.0.1,localhost
INTERNAL_IPS=127.0.0.1

# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# Email Configuration
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Payment Gateway (Optional)
RAZOR_KEY_ID=your_razorpay_key_id
RAZOR_KEY_SECRET=your_razorpay_secret
```

### 5. Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic
```

### 8. Start Redis Server
```bash
# Windows (if installed via installer)
redis-server

# Linux
sudo systemctl start redis
```

### 9. Start Celery Worker (Optional)
```bash
celery -A ppuu worker --loglevel=info
```

### 10. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 📁 Project Structure

```
ppuu/
├── account/          # User authentication and profiles
├── badge/            # Badge management system
├── base/             # Core models and utilities
├── blog/             # Blog and announcements
├── certificate/      # Digital certificate system
├── contact/          # Contact and inquiry management
├── events/           # Event management core
├── memories/         # Photo/video gallery
├── payment/          # Payment processing
├── question_papers/  # Academic resource repository
├── review/           # Reviews, polls, and Q&A
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates
├── media/            # User uploaded files
└── ppuu/             # Project configuration
```

## 🎮 Usage Guide

### For Students
1. **Register/Login**: Create account with university email
2. **Browse Events**: Explore upcoming events and activities
3. **Register for Events**: Sign up for events of interest
4. **Get Tickets**: Receive digital tickets via email
5. **Attend Events**: Show QR code ticket for entry
6. **Receive Certificates**: Get digital certificates post-event
7. **Rate & Review**: Provide feedback on attended events

### For Event Coordinators
1. **Create Events**: Set up new events with all details
2. **Manage Registrations**: Monitor and control event registrations
3. **Track Attendance**: Mark attendance during events
4. **Distribute Certificates**: Issue certificates to participants
5. **Publish Results**: Announce competition winners
6. **Analyze Performance**: Review event statistics and feedback

### For Administrators
1. **User Management**: Oversee all user accounts and permissions
2. **Content Moderation**: Review and approve blog posts and content
3. **System Configuration**: Manage courses, sections, and academic years
4. **Resource Management**: Upload and organize question papers
5. **Analytics Dashboard**: Monitor overall platform usage and performance

## 🔐 Security Features

- **CSRF Protection**: Built-in Django CSRF middleware
- **SQL Injection Prevention**: Django ORM protection
- **Secure Password Handling**: Django's built-in password hashing
- **Email Verification**: Account verification via email tokens
- **Session Security**: Redis-based secure session management
- **File Upload Validation**: Secure file handling and validation

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Set `DEBUG=False` in production
2. **Database**: Use production-grade MySQL configuration
3. **Static Files**: Configure proper static file serving
4. **SSL Certificate**: Enable HTTPS for secure communication
5. **Monitoring**: Set up logging and error tracking
6. **Backup Strategy**: Implement regular database backups

### Recommended Deployment Stack
- **Web Server**: Nginx
- **WSGI Server**: Gunicorn
- **Database**: MySQL 8.0+
- **Cache**: Redis
- **SSL**: Let's Encrypt
- **Monitoring**: Django Debug Toolbar (development only)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and queries:
- **Email**: support@eventniti.com
- **Documentation**: [Project Wiki](wiki-link)
- **Issues**: [GitHub Issues](issues-link)

## 🙏 Acknowledgments

- Django community for the excellent framework
- Contributors and beta testers
- University administration for requirements and feedback
- Open source libraries that made this project possible

---

**Event Niti** - Streamlining University Event Management 🎓