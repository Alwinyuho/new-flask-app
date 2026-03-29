from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os

# -------------------- APP SETUP --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# ✅ DATABASE FIX (Render PostgreSQL support)
db_url = os.getenv('DATABASE_URL')

if db_url:
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
else:
    db_url = "sqlite:///users.db"  # local fallback

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -------------------- DATABASE --------------------
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -------------------- LOGIN MANAGER --------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------- MODEL --------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- FORMS --------------------
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=50)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username already exists!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=50)])
    submit = SubmitField('Login')

# -------------------- ROUTES --------------------
@app.route('/')
def home():
    return render_template('index.html')

# -------- REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form)

# -------- DASHBOARD --------
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# -------- ADD NUMBERS --------
@app.route('/add_number', methods=['GET', 'POST'])
@login_required
def add_number():
    sum_result = None
    if request.method == 'POST':
        num1 = request.form.get('num1', type=int)
        num2 = request.form.get('num2', type=int)
        if num1 is not None and num2 is not None:
            sum_result = num1 + num2

    return render_template('add_number.html', sum_result=sum_result)

# -------- LOGOUT --------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# -------- INIT DATABASE + DEFAULT USER --------
@app.route('/init-db')
def init_db():
    db.create_all()

    # Create default user
    existing_user = User.query.filter_by(username="Alwinyuho").first()

    if not existing_user:
        hashed_password = generate_password_hash("Alwin@2469")
        new_user = User(username="Alwinyuho", password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return "Database + Default user created!"

    return "Database already initialized!"

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True)
