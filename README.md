# Modern Login Page with Notes App

A modern web application featuring a beautiful login page and a notes management system, built with Flask, HTML, CSS, and JavaScript.

## Features
- Responsive design with modern UI
- User authentication (Sign Up/Sign In)
- Secure password hashing
- Notes management system
  - Create new notes
  - View all notes
  - Delete notes
- SQLite database for data persistence
- Session management
- Clean and intuitive user interface

## Project Structure
```
project_folder/
├── app.py              # Flask application
├── static/
│   └── style.css      # Styles for the application
├── templates/
│   ├── index.html     # Login/Signup page
│   └── notes.html     # Notes management page
└── requirements.txt    # Python dependencies
```

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd <project-folder>
```

2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Dependencies
- Flask==2.3.3
- Flask-SQLAlchemy==3.1.1
- Flask-Login==0.6.2
- Flask-WTF==1.1.1
- Werkzeug==2.3.7
- python-dotenv==1.0.0

## Features in Detail

### Authentication
- User registration with email, name, and password
- Secure login system
- Password hashing for security
- Session management

### Notes Management
- Create new notes with title and content
- View all notes in a responsive grid layout
- Delete unwanted notes
- Notes are associated with user accounts
- Real-time updates

### UI/UX
- Modern gradient background
- Smooth animations
- Responsive design
- Social media integration buttons
- Clean and intuitive interface

## Security Features
- Password hashing using Werkzeug
- Session-based authentication
- Protected routes
- SQL injection prevention through SQLAlchemy
- CSRF protection

## Author
Gaurav Sonawane

