# Modern Note Taking Application

A full-stack note-taking application with a beautiful UI, built with Flask and modern web technologies.

## Features

- 🔐 Secure user authentication
- 📝 Create, read, update, and delete notes
- 🖼️ Image upload support
- 🔍 Search functionality
- 📱 Responsive design
- 🎨 Modern UI with purple/white theme

## Project Structure

```
.
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   └── uploads/
│   └── templates/
│       ├── index.html
│       └── dashboard.html
└── README.md
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with the following content:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///notes.db
   FLASK_ENV=development
   FLASK_APP=app.py
   ```

5. Run the Flask application:
   ```bash
   flask run
   ```

The backend will be available at `http://localhost:5000`

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Register a new account or login with existing credentials
3. After logging in, you'll be redirected to the dashboard
4. Create, edit, and delete notes
5. Upload images to your notes
6. Search through your notes using the search bar

## Features in Detail

### Authentication
- Secure login and registration
- Password hashing
- Session management

### Notes Management
- Create new notes with title and content
- Upload images to notes
- Edit existing notes
- Delete notes
- Search through notes

### User Interface
- Modern purple and white theme
- Responsive design for all devices
- Clean and intuitive layout
- Toast notifications for actions
- Image preview before upload

## Security Features

- Password hashing using Werkzeug
- CSRF protection
- Secure file upload handling
- Input validation
- SQL injection prevention

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Author
Gaurav Sonawane

## Deployment on Render

### Prerequisites
1. A Render account (sign up at https://render.com)
2. Git installed on your local machine
3. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

### Deployment Steps

1. **Prepare Your Application**
   - Ensure all files are committed to your repository
   - Make sure `requirements.txt` and `gunicorn.conf.py` are in your root directory
   - Verify your `render.yaml` configuration

2. **Deploy on Render**
   - Log in to your Render dashboard
   - Click "New +" and select "Web Service"
   - Connect your repository
   - Configure your service:
     - Name: `modern-notes-app` (or your preferred name)
     - Environment: `Python`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Add Environment Variables:
     - `SECRET_KEY`: Generate a secure random key
     - `DATABASE_URL`: Your database URL
     - `FLASK_ENV`: Set to `production`

3. **Database Setup**
   - For production, it's recommended to use a PostgreSQL database
   - You can add a PostgreSQL database from Render's dashboard
   - Update your `DATABASE_URL` environment variable with the new database URL

4. **Verify Deployment**
   - Once deployed, Render will provide you with a URL
   - Test all features:
     - User registration
     - Login
     - Note creation
     - Image upload
     - Search functionality

### Important Notes
- Render's free tier has some limitations:
  - Services spin down after 15 minutes of inactivity
  - Limited bandwidth and compute hours
- For production use, consider upgrading to a paid plan
- Keep your `SECRET_KEY` secure and never commit it to your repository
- Regularly backup your database

