from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, session as db_session 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Group10'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
class Car(db.Model):
    __tablename__ = "cars"
    vin = db.Column(db.String(50), unique=True, primary_key=True)
    cartype = db.Column(db.String(50))
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    ppd = db.Column(db.Integer, nullable=False)
    mpg = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    current_customer_cid = db.Column(db.Integer, unique=True)
    location = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    
    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)

# Initialize the database
with app.app_context():
    db.create_all()
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    car = Car(vin="1FT8W2BT9NEC70388", cartype="Pickup", make="Ford", model="F-250", year=2022, seats=4, ppd=155, mpg=24, mileage=89041, current_customer_cid=None, location="Raleigh", image="F-250_2022.jpg")
    session.add(car)
    session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    from flask import session  
    session.clear()  
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')

    # Check if user with this email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already in use.', 'error')
        return redirect(url_for('index'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=hashed_password)
    
    db.session.add(new_user)
    try:
        db.session.commit()
        flash('Account created successfully!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error creating account. Email may already be in use.', 'error')
    
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('dashboard'))

    flash('Login failed. Check your credentials.', 'error')
    return redirect(url_for('index'))

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/browse_cars')
def browse_cars():
    category_name = request.args.get('category', 'All')
    if category_name != 'All':
        cars = Car.query.filter_by(cartype=category_name).all()
    else:
        cars = Car.query.all()
    return render_template('browse_cars.html', cars=cars, category_name=category_name)



@app.route('/book_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def book_car(car_id):
    car = Car.query.get_or_404(car_id)
    if request.method == 'POST':
        # Handle the booking logic here
        flash('Car booked successfully!', 'success')
        return redirect(url_for('dashboard'))
    # display a booking form or confirmation page
    return render_template('book_car.html', car=car)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
