from flask import Flask, render_template, url_for, redirect,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/users'
app.config['SECRET_KEY'] = 'Ogodoremmanuel'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=16)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=16)])
    submit = SubmitField('Login')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password. Please try again.', 'error')
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Define a list of subjects with their subject code and names
subjects = [
    {"code": "IS", "name": "Information System"},
    {"code": "IAI", "name": "Internet & Intranet"},
    {"code": "EPP", "name": "Engineering Professional Practice"},
    {"code": "SAM", "name": "Simulation and Modeling"},
    {"code": "BD", "name": "Big Data"},
    {"code": "MM", "name": "MultiMedia"}
]

@app.route('/')
def index():
    return render_template('index.html', subjects=subjects)

@app.route('/attendance/<subject_code>', methods=['GET'])
def subject_page(subject_code):
    # Here you can render a page with options to take attendance or view attendance report
    return render_template('subject.html', subject_code=subject_code)

@app.route('/attendance/<subject_code>/take', methods=['GET'])


@app.route('/attendance/<subject_code>/report', methods=['GET'])
def view_report(subject_code):
    # Logic to view attendance report for the specified subject
    return "View attendance report for subject {}".format(subject_code)

@app.route('/take_attendance', methods=['GET'])
def take_attendance():
    return render_template('take_attendance.html')

from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
import os

app.config['UPLOAD_FOLDER'] = 'data'  # Folder where uploaded images will be stored

# Function to save the uploaded image file to the server
def save_uploaded_image(image_data):
    try:
        # Decode the base64-encoded image data
        image_data = image_data.split(',')[1]  # Remove the "data:image/png;base64," prefix
        image_bytes = image_data.encode('utf-8')
        with open(os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.png'), 'wb') as f:
            f.write(image_bytes)
        return True
    except Exception as e:
        print('Error saving uploaded image:', str(e))
        return False

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Get the image data from the request JSON
        image_data = request.json.get('image_data')
        if image_data:
            # Save the uploaded image to the server
            if save_uploaded_image(image_data):
                # Image was successfully saved
                return jsonify({'success': True, 'message': 'Image uploaded successfully.'}), 200
            else:
                # Error occurred while saving the image
                return jsonify({'success': False, 'message': 'Error uploading image.'}), 500
        else:
            # Image data not found in the request
            return jsonify({'success': False, 'message': 'No image data found in the request.'}), 400
    except Exception as e:
        # Error occurred while processing the request
        print('Error processing image:', str(e))
        return jsonify({'success': False, 'message': 'Error processing image.'}), 500
    
import base64
import uuid  # Import UUID module for generating unique filenames

# Function to save the uploaded image file to the server
def save_uploaded_image(image_data):
    try:
        # Decode the base64-encoded image data
        image_data = image_data.split(',')[1]  # Remove the "data:image/png;base64," prefix
        image_bytes = base64.b64decode(image_data)
        
        # Generate a unique filename for the image
        image_filename = str(uuid.uuid4()) + '.png'

        # Save the image data to a file with the unique filename
        with open(os.path.join(app.config['UPLOAD_FOLDER'], image_filename), 'wb') as f:
            f.write(image_bytes)
        
        return True, image_filename  # Return success status and the filename
    except Exception as e:
        print('Error saving uploaded image:', str(e))
        return False, None



if __name__ == '__main__':
    app.run(debug=True)


