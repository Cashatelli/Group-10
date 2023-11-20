from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, session as db_session 
from flask import session
from datetime import datetime, date


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
    location = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.String(50), db.ForeignKey('cars.vin'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    user = db.relationship('User', backref='bookings')
    car = db.relationship('Car', backref='bookings')

# Initialize the database
with app.app_context():
    db.create_all()
    db.session.query(Car).delete()

    cars = [ 
        #Pickup Cars
        Car(vin="1FT7W2B64JEB65645", cartype="Pickup", make="Ford", model="F-250", year=2018, seats=4, ppd=102, mpg=21, mileage=99103, location="Winterville", image="F-250_2018.jpg"),
        Car(vin="1FT8W2BT9NEC70388", cartype="Pickup", make="Ford", model="F-250", year=2022, seats=4, ppd=155, mpg=24, mileage=89041, location="Raleigh", image="F-250_2022.jpg"),
        Car(vin="1C6HJTFG7NL119666", cartype="Pickup", make="Jeep", model="Gladiator", year=2022, seats=4, ppd=165, mpg=20, mileage=20100, location="Winterville", image="jeep_gladiator_2022.jpg"),
        Car(vin="1GC4YUEY6MF190132", cartype="Pickup", make="Chevrolet", model="Silverado", year=2021, seats=4, ppd=120, mpg=21, mileage=89095, location="Raleigh", image="chevrolet_silverado_2022.jpg"),
        Car(vin="1C6RREFT6MN543610", cartype="Pickup", make="Ram", model="1500", year=2021, seats=4, ppd=98, mpg=19, mileage=98874, location="Winterville", image="ram_1500_2021.jpg"),
        Car(vin="5FPYK3F72KB028445", cartype="Pickup", make="Honda", model="Ridgeline", year=2019, seats=4, ppd=115, mpg=22, mileage=68798, location="Raleigh", image="honda_ridgeline_2019.jpg"),
        Car(vin="3C6RR6LT3JG146144", cartype="Pickup", make="Ram", model="1500", year=2018, seats=4, ppd=88, mpg=19, mileage=124794, location="Charlotte", image="ram_1500_2018.jpg"),
        Car(vin="1C6SRFBTXKN733890", cartype="Pickup", make="Ram", model="1500", year=2019, seats=4, ppd=95, mpg=18, mileage=72380, location="Raleigh", image="ram_1500_2019.jpg"),   
        Car(vin="5NTJEDAF7NH011122", cartype="Pickup", make="Hyundai", model="Santa_Cruz", year=2022, seats=4, ppd=143, mpg=24, mileage=13159, location="Charlotte", image="hyundai_santacruz_2022.jpg"),
        Car(vin="1FTEW1EGXJFE55694", cartype="Pickup", make="Ford", model="F-150", year=2018, seats=4, ppd=118, mpg=19, mileage=86410, location="Charlotte", image="ford_f-150_2018.jpg"),
        Car(vin="1GTN1LEC4GZ146768", cartype="Pickup", make="GMC", model="Sierra_1500", year=2016, seats=2, ppd=79, mpg=20, mileage=118713, location="Charlotte", image="gmc_serria_2016.jpg"),
        Car(vin="1GTN1LEC1HZ905958", cartype="Pickup", make="GMC", model="Sierra_1500", year=2017, seats=2, ppd=75, mpg=20, mileage=101170, location="Raleigh", image="gmc_serria_2017.jpg"),
        Car(vin="3C6JR6DT6GG239518", cartype="Pickup", make="Ram", model="1500", year=2016, seats=2, ppd=94, mpg=19, mileage=49084, location="Winterville", image="ram_1500_2016.jpg"),
        Car(vin="1FTMF1C88GKF91569", cartype="Pickup", make="Ford", model="F-150", year=2016, seats=2, ppd=90, mpg=21, mileage=97477, location="Charlotte", image="ford_F-150_2016.jpg"),
        #Sedan Cars
        Car(vin="WBAKB8C51CC964616", cartype="Sedan", make="BMW", model="7_Series", year=2012, seats=5, ppd=75, mpg=18, mileage=91767, location="Raleigh", image="Sedan_image.jpg"),        
        Car(vin="1G11B5SA1DF256175", cartype="Sedan", make="Chevrolet", model="Malibu", year=2013, seats=5, ppd=88, mpg=27, mileage=137018, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="W1KWF8DBXMR642820", cartype="Sedan", make="Mercedes-Benz", model="C-Class", year=2021, seats=5, ppd=126, mpg=29, mileage=35799, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="7JR102FK9LG045640", cartype="Sedan", make="Volvo", model="S60", year=2020, seats=5, ppd=110, mpg=29, mileage=36145, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="5NPE34AF0KH785469", cartype="Sedan", make="Hyundai", model="Sonata", year=2019, seats=5, ppd=97, mpg=29, mileage=120714, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="1G6DN5RW3M0110685", cartype="Sedan", make="Cadillac", model="CT5", year=2021, seats=5, ppd=131, mpg=24, mileage=20698, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="19UUB2F39GA012467", cartype="Sedan", make="Acura", model="TLX", year=2016, seats=5, ppd=83, mpg=28, mileage=127952, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="KNAE35LD3N6099133", cartype="Sedan", make="Kia", model="Stinger", year=2022, seats=5, ppd=103, mpg=27, mileage=32002, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="4T1K61AK9MU614780", cartype="Sedan", make="Toyota", model="Camry", year=2021, seats=5, ppd=78, mpg=32, mileage=47272, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="3FA6P0HD0LR143456", cartype="Sedan", make="Ford", model="Fusion", year=2020, seats=5, ppd=91, mpg=28, mileage=40977, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="3KPF54AD3NE448185", cartype="Sedan", make="Kia", model="Forte", year=2022, seats=5, ppd=99, mpg=35, mileage=11564, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="7JRBR0FM4NG179054", cartype="Sedan", make="Volvo", model="S60", year=2022, seats=5, ppd=106, mpg=31, mileage=15365, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="KMHLN4AJ0PU047489", cartype="Sedan", make="Hyundai", model="Elantra", year=2023, seats=5, ppd=114, mpg=51, mileage=10820, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="3KPF24AD8ME359039", cartype="Sedan", make="Kia", model="Forte", year=2021, seats=5, ppd=81, mpg=34, mileage=17850, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="5XXGT4L33KG330445", cartype="Sedan", make="Kia", model="Optima", year=2019, seats=5, ppd=77, mpg=29, mileage=37976, location="Charlotte", image="Sedan_image.jpg"),
        #Suv, ect
        Car(vin="LRBFXESX6HD117758", cartype="Suv", make="Buick", model="Envision", year=2017, seats=5, ppd=80, mpd=22, mileage=32996, location="Boone", image="buick_en_2017.jpg"),
        Car(vin="1FMCU0F6XLUA23677", cartype="Suv", make="Ford", model="Escape S", year=2020, seats=5, ppd=92, mpg=27, mileage=77258, location="Charlotte", image="ford_escape_2020.jpg"),
        Car(vin="JF2GTHMC4N8213990", cartype="Suv", make="Subaru", model="Crosstrek", year=2022, seats=5, ppd=95, mpg=27, mileage=20308, location="Raleigh", image="subaru_cross_2022.jpg"),
        Car(vin="3FMCR9B67MRA12544", cartype="Suv", make="Ford", model="Bronco Sport", year=2021, seats=5, ppd=110, mpg=25, mileage=126954, location="Greenville", image="ford_bronco_2021.jpg"),
        Car(vin="JN8AY2ND3H9006018", cartype="Suv", make="Nissan", model="Armada SL", year=2017, seats=5, ppd=82, mpg=19, mileage=86400, location="Durham", image="nissan_armada_2017.jpg"),
        Car(vin="1C4BJWFG5GL218652", cartype="Suv", make="Jeep", model="Wrangler Rubicon", year=2016, seats=5, ppd=97, mpg=20, mileage=80266, location="Greensboro", image="jeep_wrang_2016.jpg"),
        Car(vin="JTEMU5JR1M5865497", cartype="Suv", make="Toyota", model="4Runner SR5", year=2021, seats=5, ppd=89, mpg=18, mileage=127934, location="Asheville", image="toyota_4runner_2021.jpg"),
        Car(vin="5LMCJ1CA4PUL10877", cartype="Suv", make="Lincoln", model="Corsair", year=2023, seats=5, ppd=110, mpg=22, mileage=39902, location="Wilmington", image="lincoln_corsair_2023.jpg"),
        Car(vin="1FMEE5DH9MLA93492", cartype="Suv", make="Ford", model="Bronco Badlands", year=2021, seats=5, ppd=121, mpg=18, mileage=41272, location="Durham", image="ford_bronco_badlands_2021.jpg"),
        Car(vin="1GKS1BKD0NR264988", cartype="Suv", make="GMC", model="Yukon SLT", year=2022, seats=5, ppd=87, mpg=20, mileage=86977, location="Raleigh", image="gmc_yukon_2022.jpg"),
        Car(vin="KL79MNSL4PB194091", cartype="Suv", make="Chevrolet", model="TrailBlazer LS", year=2023, seats=5, ppd=99, mpg=26, mileage=37564, location="Greenville", image="chevrolet_trailblazer_2023.jpg"),
        Car(vin="5XYKT3A69DG406850", cartype="Suv", make="Kia", model="Sorento LX", year=2013, seats=5, ppd=68, mpg=23, mileage=62365, location="Boone", image="kia_sorento_2013.jpg"),
        Car(vin="JTEAAAH1MJ0032544", cartype="Suv", make="Toyota", model="Venza LE", year=2021, seats=5, ppd=91, mpg=35, mileage=43820, location="Ashville", image="toyota_venza_2021.jpg"),
        Car(vin="WA1ECCFS9HR006677", cartype="Suv", make="Audi", model="Q3", year=2017, seats=5, ppd=83, mpg=22, mileage=52850, location="Charlotte", image="audi_q3_2017.jpg"),
        Car(vin="4S4WMAPD9M3423270", cartype="Suv", make="Subaru", model="Ascent", year=2021, seats=5, ppd=75, mpg=24, mileage=72976, location="Wilmington", image="subaru_ascent.jpg")
    ]

    for car in cars:
        db.session.add(car)
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
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

@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('terms-and-conditions.html')  # Ensure this template exists

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
    today = date.today()

    if category_name != 'All':
        cars = Car.query.filter_by(cartype=category_name).all()
    else:
        cars = Car.query.all()

    for car in cars:
        # Check if the car has any active bookings for today
        active_bookings = Booking.query.filter(
            Booking.car_id == car.vin,
            Booking.start_date <= today,
            Booking.end_date >= today
        ).all()
        car.available = len(active_bookings) == 0

    return render_template('browse_cars.html', cars=cars, category_name=category_name)

from datetime import datetime

@app.route('/book_car/<string:car_vin>', methods=['GET', 'POST'])
@login_required
def book_car(car_vin):
    car = Car.query.get_or_404(car_vin)

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date >= end_date:
            flash('End date must be after start date.', 'error')
            return render_template('book_car.html', car=car)

        total_days = (end_date - start_date).days
        total_cost = total_days * car.ppd

        new_booking = Booking(
            user_id=current_user.id,
            car_id=car.vin,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_booking)
        db.session.commit()

        flash(f'Car booked successfully for {total_days} days. Total cost: ${total_cost}', 'success')
        return redirect(url_for('current_reservations'))

    return render_template('book_car.html', car=car)
      
@app.route('/current_reservations')
@login_required
def current_reservations():
    user_id = current_user.id
    reservations = Booking.query.filter_by(user_id=user_id).all()
    today = datetime.today().date()

    return render_template('current_reservations.html', reservations=reservations, today=today)
@app.route('/cancel_reservation/<int:reservation_id>')
@login_required
def cancel_reservation(reservation_id):
    reservation = Booking.query.get_or_404(reservation_id)
    if reservation.user_id != current_user.id:
        abort(403)  # Unauthorized access

    # Logic to cancel the reservation
    db.session.delete(reservation)
    db.session.commit()

    flash('Reservation canceled successfully', 'success')
    return redirect(url_for('current_reservations'))


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
