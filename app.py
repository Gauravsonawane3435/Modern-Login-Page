from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

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
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': note.id,
        'title': note.title,
        'content': note.content
    } for note in notes])

@app.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    data = request.get_json()
    new_note = Note(
        title=data['title'],
        content=data['content'],
        user_id=current_user.id
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify({
        'id': new_note.id,
        'title': new_note.title,
        'content': new_note.content
    }), 201

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(note)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 