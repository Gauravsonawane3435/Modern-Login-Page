from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import time
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'hsidferfbh3dbsyh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)

# Note Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return jsonify({'message': 'Login successful'}), 200

        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/notes')
@login_required
def notes():
    return render_template('notes.html')

@app.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    try:
        notes = Note.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'image_path': note.image_path
        } for note in notes])
    except Exception as e:
        app.logger.error(f"Error in get_notes: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    try:
        if not request.form:
            return jsonify({'error': 'No form data received'}), 400

        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400

        image_path = None
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to make it unique
                filename = f"{int(time.time())}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_path = f"uploads/{filename}"

        new_note = Note(
            title=title,
            content=content,
            image_path=image_path,
            user_id=current_user.id
        )
        db.session.add(new_note)
        db.session.commit()
        
        return jsonify({
            'id': new_note.id,
            'title': new_note.title,
            'content': new_note.content,
            'image_path': new_note.image_path
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in create_note: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    try:
        note = db.session.get(Note, note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
            
        if note.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Delete associated image if exists
        if note.image_path:
            try:
                os.remove(os.path.join(app.static_folder, note.image_path))
            except:
                pass  # Ignore if file doesn't exist
                
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in delete_note: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Initialize database
def init_db():
    with app.app_context():
        # Check if the database file exists
        db_exists = os.path.exists('notes.db')
        
        # Create all tables
        db.create_all()
        
        # If the database already existed, check if we need to add the image_path column
        if db_exists:
            try:
                # Try to access the image_path column
                db.session.execute('SELECT image_path FROM note LIMIT 1')
            except sqlite3.OperationalError:
                # If the column doesn't exist, add it
                db.session.execute('ALTER TABLE note ADD COLUMN image_path VARCHAR(200)')
                db.session.commit()
                app.logger.info("Added image_path column to note table")

        app.logger.info("Database initialized successfully")

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 