from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, session as db_session 
from flask import session
from datetime import datetime, date
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
from sqlalchemy import and_, or_
from flask_login import current_user
from werkzeug.security import generate_password_hash
from flask import render_template

import math
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Group10'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Mail Information
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'rentacar5142@gmail.com'
app.config['MAIL_PASSWORD'] = 'okin mldr iwbm cdqn'
app.config['MAIL_DEFAULT_SENDER'] = 'rentacar5142@gmail.com'
mail = Mail(app)

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
        Car(vin="1FT7W2B64JEB65645", cartype="Pickup", make="Ford", model="F-250", year=2018, seats=4, ppd=102, mpg=21, mileage=99103, location="Raleigh", image="F-250_2018.jpg"),
        Car(vin="1FT8W2BT9NEC70388", cartype="Pickup", make="Ford", model="F-250", year=2022, seats=4, ppd=155, mpg=24, mileage=89041, location="Durham", image="F-250_2022.jpg"),
        Car(vin="1C6HJTFG7NL119666", cartype="Pickup", make="Jeep", model="Gladiator", year=2022, seats=4, ppd=165, mpg=20, mileage=20100, location="Asheville", image="jeep_gladiator_2022.jpg"),
        Car(vin="1GC4YUEY6MF190132", cartype="Pickup", make="Chevrolet", model="Silverado", year=2021, seats=4, ppd=120, mpg=21, mileage=89095, location="Boone", image="chevrolet_silverado_2022.jpg"),
        Car(vin="1C6RREFT6MN543610", cartype="Pickup", make="Ram", model="1500", year=2021, seats=4, ppd=98, mpg=19, mileage=98874, location="Durham", image="ram_1500_2021.jpg"),
        Car(vin="5FPYK3F72KB028445", cartype="Pickup", make="Honda", model="Ridgeline", year=2019, seats=4, ppd=115, mpg=22, mileage=68798, location="Raleigh", image="honda_ridgeline_2019.jpg"),
        Car(vin="3C6RR6LT3JG146144", cartype="Pickup", make="Ram", model="1500", year=2018, seats=4, ppd=88, mpg=19, mileage=124794, location="Charlotte", image="ram_1500_2018.jpg"),
        Car(vin="1C6SRFBTXKN733890", cartype="Pickup", make="Ram", model="1500", year=2019, seats=4, ppd=95, mpg=18, mileage=72380, location="Wilmington", image="ram_1500_2019.jpg"),   
        Car(vin="5NTJEDAF7NH011122", cartype="Pickup", make="Hyundai", model="Santa_Cruz", year=2022, seats=4, ppd=143, mpg=24, mileage=13159, location="Asheville", image="hyundai_santacruz_2022.jpg"),
        Car(vin="1FTEW1EGXJFE55694", cartype="Pickup", make="Ford", model="F-150", year=2018, seats=4, ppd=118, mpg=19, mileage=86410, location="Durham", image="ford_f-150_2018.jpg"),
        Car(vin="1GTN1LEC4GZ146768", cartype="Pickup", make="GMC", model="Sierra_1500", year=2016, seats=2, ppd=79, mpg=20, mileage=118713, location="Greenville", image="gmc_serria_2016.jpg"),
        Car(vin="1GTN1LEC1HZ905958", cartype="Pickup", make="GMC", model="Sierra_1500", year=2017, seats=2, ppd=75, mpg=20, mileage=101170, location="Raleigh", image="gmc_serria_2017.jpg"),
        Car(vin="3C6JR6DT6GG239518", cartype="Pickup", make="Ram", model="1500", year=2016, seats=2, ppd=94, mpg=19, mileage=49084, location="Boone", image="ram_1500_2016.jpg"),
        Car(vin="1FTMF1C88GKF91569", cartype="Pickup", make="Ford", model="F-150", year=2016, seats=2, ppd=90, mpg=21, mileage=97477, location="Charlotte", image="ford_F-150_2016.jpg"),
        #Sedan Cars
        Car(vin="WBAKB8C51CC964616", cartype="Sedan", make="BMW", model="7_Series", year=2012, seats=5, ppd=75, mpg=18, mileage=91767, location="Raleigh", image="bmw_7series_2012.jpg"),        
        Car(vin="1G11B5SA1DF256175", cartype="Sedan", make="Chevrolet", model="Malibu", year=2013, seats=5, ppd=88, mpg=27, mileage=137018, location="Charlotte", image="chevrolet_malibu_2013.jpg"),
        Car(vin="W1KWF8DBXMR642820", cartype="Sedan", make="Mercedes-Benz", model="C-Class", year=2021, seats=5, ppd=126, mpg=29, mileage=35799, location="Wilmington", image="mercedes-benz_c-class_2021.jpg"),
        Car(vin="7JR102FK9LG045640", cartype="Sedan", make="Volvo", model="S60", year=2020, seats=5, ppd=110, mpg=29, mileage=36145, location="Durham", image="volvo_s60_2020.jpg"),
        Car(vin="5NPE34AF0KH785469", cartype="Sedan", make="Hyundai", model="Sonata", year=2019, seats=5, ppd=97, mpg=29, mileage=120714, location="Boone", image="hyundai_sonata_2019.jpg"),
        Car(vin="1G6DN5RW3M0110685", cartype="Sedan", make="Cadillac", model="CT5", year=2021, seats=5, ppd=131, mpg=24, mileage=20698, location="Asheville", image="cadillac_ct5_2021.jpg"),
        Car(vin="19UUB2F39GA012467", cartype="Sedan", make="Acura", model="TLX", year=2016, seats=5, ppd=83, mpg=28, mileage=127952, location="Greenville", image="acura_tlx_2016.jpg"),
        Car(vin="KNAE35LD3N6099133", cartype="Sedan", make="Kia", model="Stinger", year=2022, seats=5, ppd=103, mpg=27, mileage=32002, location="Charlotte", image="kia_stinger_2022.jpg"),
        Car(vin="4T1K61AK9MU614780", cartype="Sedan", make="Toyota", model="Camry", year=2021, seats=5, ppd=78, mpg=32, mileage=47272, location="Raleigh", image="toyota_camry_2021.jpg"),
        Car(vin="3FA6P0HD0LR143456", cartype="Sedan", make="Ford", model="Fusion", year=2020, seats=5, ppd=91, mpg=28, mileage=40977, location="Greenville", image="ford_fusion_2020.jpg"),
        Car(vin="3KPF54AD3NE448185", cartype="Sedan", make="Kia", model="Forte", year=2022, seats=5, ppd=99, mpg=35, mileage=11564, location="Boone", image="kia_forte_2022.jpg"),
        Car(vin="7JRBR0FM4NG179054", cartype="Sedan", make="Volvo", model="S60", year=2022, seats=5, ppd=106, mpg=31, mileage=15365, location="Durham", image="volvo_s60_2022.jpg"),
        Car(vin="KMHLN4AJ0PU047489", cartype="Sedan", make="Hyundai", model="Elantra", year=2023, seats=5, ppd=114, mpg=51, mileage=10820, location="Asheville", image="hyundai_elantra_2023.jpg"),
        Car(vin="3KPF24AD8ME359039", cartype="Sedan", make="Kia", model="Forte", year=2021, seats=5, ppd=81, mpg=34, mileage=17850, location="Raleigh", image="kia_forte_2021.jpg"),
        Car(vin="5XXGT4L33KG330445", cartype="Sedan", make="Kia", model="Optima", year=2019, seats=5, ppd=77, mpg=29, mileage=37976, location="Charlotte", image="kia_optima_2019.jpg"),
        #Suv
        Car(vin="LRBFXESX6HD117758", cartype="SUV", make="Buick", model="Envision", year=2017, seats=5, ppd=80, mpg=22, mileage=32996, location="Boone", image="buick_en_2017.jpg"),
        Car(vin="1FMCU0F6XLUA23677", cartype="SUV", make="Ford", model="Escape S", year=2020, seats=5, ppd=92, mpg=27, mileage=77258, location="Charlotte", image="ford_escape_2020.jpg"),
        Car(vin="JF2GTHMC4N8213990", cartype="SUV", make="Subaru", model="Crosstrek", year=2022, seats=5, ppd=95, mpg=27, mileage=20308, location="Raleigh", image="subaru_cross_2022.jpg"),
        Car(vin="3FMCR9B67MRA12544", cartype="SUV", make="Ford", model="Bronco Sport", year=2021, seats=5, ppd=110, mpg=25, mileage=126954, location="Greenville", image="ford_bronco_2021.jpg"),
        Car(vin="JN8AY2ND3H9006018", cartype="SUV", make="Nissan", model="Armada SL", year=2017, seats=5, ppd=82, mpg=19, mileage=86400, location="Durham", image="nissan_armada_2017.jpg"),
        Car(vin="1C4BJWFG5GL218652", cartype="SUV", make="Jeep", model="Wrangler Rubicon", year=2016, seats=5, ppd=97, mpg=20, mileage=80266, location="Asheville", image="jeep_wrang_2016.jpg"),
        Car(vin="JTEMU5JR1M5865497", cartype="SUV", make="Toyota", model="4Runner SR5", year=2021, seats=5, ppd=89, mpg=18, mileage=127934, location="Asheville", image="toyota_4runner_2021.jpg"),
        Car(vin="5LMCJ1CA4PUL10877", cartype="SUV", make="Lincoln", model="Corsair", year=2023, seats=5, ppd=110, mpg=22, mileage=39902, location="Wilmington", image="lincoln_corsair_2023.jpg"),
        Car(vin="1FMEE5DH9MLA93492", cartype="SUV", make="Ford", model="Bronco Badlands", year=2021, seats=5, ppd=121, mpg=18, mileage=41272, location="Durham", image="ford_bronco_badlands_2021.jpg"),
        Car(vin="1GKS1BKD0NR264988", cartype="SUV", make="GMC", model="Yukon SLT", year=2022, seats=5, ppd=87, mpg=20, mileage=86977, location="Raleigh", image="gmc_yukon_2022.jpg"),
        Car(vin="KL79MNSL4PB194091", cartype="SUV", make="Chevrolet", model="TrailBlazer LS", year=2023, seats=5, ppd=99, mpg=26, mileage=37564, location="Greenville", image="chevrolet_trailblazer_2023.jpg"),
        Car(vin="5XYKT3A69DG406850", cartype="SUV", make="Kia", model="Sorento LX", year=2013, seats=5, ppd=68, mpg=23, mileage=62365, location="Boone", image="kia_sorento_2013.jpg"),
        Car(vin="JTEAAAH1MJ0032544", cartype="SUV", make="Toyota", model="Venza LE", year=2021, seats=5, ppd=91, mpg=35, mileage=43820, location="Asheville", image="toyota_venza_2021.jpg"),
        Car(vin="WA1ECCFS9HR006677", cartype="SUV", make="Audi", model="Q3", year=2017, seats=5, ppd=83, mpg=22, mileage=52850, location="Charlotte", image="audi_q3_2017.jpg"),
        Car(vin="4S4WMAPD9M3423270", cartype="SUV", make="Subaru", model="Ascent", year=2021, seats=5, ppd=75, mpg=24, mileage=72976, location="Wilmington", image="subaru_ascent.jpg"),
        #Coupe
        Car(vin="2C3CDZBT3PH527800", cartype="Coupe", make="Dodge", model="Challenger R/T", year=2023, seats=5, ppd=95, mpg=18, mileage=2567, location="Charlotte", image="dodge_challenger_2023.jpg"),
        Car(vin="1G1YM2D7XH5102245", cartype="Coupe", make="Chevrolet", model="Corvette Z51 LT3", year=2017, seats=2, ppd=90, mpg=17, mileage=3782, location="Durham", image="chev_corvette_2017.jpg"),
        Car(vin="1FA6P9TH7M5156492", cartype="Coupe", make="Ford", model="Mustang", year=2021, seats=2, ppd=83, mpg=20, mileage=836075, location="Greenville", image="ford_mustang_2021.jpg"),
        Car(vin="1G1FB1RX8H0106050", cartype="Coupe", make="Chevrolet", model="Camaro LT 1LT", year=2017, seats=2, ppd=89, mpg=22, mileage=85934, location="Asheville", image="chev_camaro_2017.jpg"),
        Car(vin="1G1YY2D75H5120754", cartype="Coupe", make="Chevrolet", model="Corvette Grand Sport LT2", year=2017, seats=2, ppd=97, mpg=16, mileage=82902, location="Wilmington", image="chev_grand_2017.jpg"),
        Car(vin="2C3DZJG1KH7023821", cartype="Coupe", make="Dodge", model="Challenger GT", year=2019, seats=2, ppd=80, mpg=19, mileage=74172, location="Raleigh", image="dodge_GT_2019.jpg"),
        Car(vin="JF1ZCAC17L9702394", cartype="Coupe", make="Subaru", model="BRZ Limited", year=2020, seats=2, ppd=82, mpg=22, mileage=24928, location="Raleigh", image="subaru_brz_2020.jpg"),
        Car(vin="1FA6P8SJ5M5502138", cartype="Coupe", make="Ford", model="Mustang Shelby GT500", year=2021, seats=2, ppd=99, mpg=15, mileage=34254, location="Greenville", image="ford_shelby_2020.jpg"),
        Car(vin="JF1ZCAC14H9601370", cartype="Coupe", make="Subaru", model="BRZ", year=2017, seats=2, ppd=73, mpg=25, mileage=17734, location="Asheville", image="subaru_brz_2017.jpg"),
        Car(vin="1FA6P8CF5N5143126", cartype="Coupe", make="Ford", model="Mustang GT", year=2022, seats=2, ppd=92, mpg=26, mileage=3199, location="Durham", image="ford_must_2022.jpg"),
        Car(vin="WBA3N5C53Fk197971", cartype="Coupe", make="BMW", model="4 Series 428i xDrive", year=2015, seats=2, ppd=70, mpg=27, mileage=120728, location="Charlotte", image="bmw_4series_2022.jpg"),
        Car(vin="WAUWFAFRXBA023588", cartype="Coupe", make="Audi", model="A5 Prestige", year=2020, seats=2, ppd=65, mpg=24, mileage=123527, location="Wilmington", image="audi_prestige_2020.jpg"),
        Car(vin="1ZVBP8CU0PJU89322", cartype="Coupe", make="Ford", model="Boss 302", year="2013", seats=2, ppd=78, mpg=18, mileage=4265, location="Raleigh", image="mustang_boss_2013.jpg"),
        Car(vin="ADBCDZBT3PH527800", cartype="Coupe", make="BMW", model="4 Series 430i", year=2023, seats=2, ppd=98, mpg=26, mileage=23367, location="Boone", image="bmw_4series_2023.jpg"),
        Car(vin="1G134GNSUH5102245", cartype="Coupe", make="Mercedes-Benz", model="E-Class E 350", year=2022, seats=2, ppd=68, mpg=22, mileage=11182, location="Durham", image="benz_2022.jpg"),
        #Convertible
        Car(vin="1G1FK360M01393373", cartype="Convertible", make="Chevrolet", model="Camaro ZL1", year=2021, seats=2, ppd=120, mpg=19, mileage=8567, location="Charlotte", image="chev_zl1_2021.jpg"),
        Car(vin="1G1YB3D41R5101696", cartype="Convertible", make="Chevrolet", model="Corvette LT2", year=2022, seats=2, ppd=135, mpg=18, mileage=121, location="Durham", image="chev_lt2_2022.jpg"),
        Car(vin="1DJ7F837M515649E2", cartype="Convertible", make="Mini Cooper", model="S", year=2022, seats=4, ppd=85, mpg=22, mileage=13075, location="Wilmington", image="mini_coop_2022.jpg"),
        Car(vin="DE1FB1RX811206050", cartype="Convertible", make="Mazda", model="Miada Sport", year=2017, seats=2, ppd=82, mpg=20, mileage=89934, location="Asheville", image="mazda_sport_2017.jpg"),
        Car(vin="WBA23AT04NCJ52318", cartype="Convertible", make="BMW", model="4 Series 430i", year=2022, seats=4, ppd=97, mpg=25, mileage=1902, location="Durham", image="bmw_430i_2022.jpg"),
        Car(vin="SCBDG4ZG2LC073824", cartype="Convertible", make="Bentley", model="Continental GT", year=2020, seats=4, ppd=80, mpg=22, mileage=14172, location="Raleigh", image="bentley_2020.jpg"),
        Car(vin="SCFRMFCW3KGM60305", cartype="Convertible", make="Aston Matin", model="DB11", year=2019, seats=4, ppd=105, mpg=26, mileage=34928, location="Raleigh", image="aston_2020.jpg"),
        Car(vin="WP0CB2A9XCS754452", cartype="Convertible", make="Porsche", model="911 Carrera GTS", year=2018, seats=2, ppd=99, mpg=23, mileage=33754, location="Greenville", image="porsche_911_2012.jpg"),
        Car(vin="1G1FE3D79N0128855", cartype="Convertible", make="Chevrolet", model="Camaro SS 1SS", year=2022, seats=4, ppd=79, mpg=19, mileage=13734, location="Boone", image="chev_camaroSS_2022.jpg"),
        Car(vin="WBAHF3C07NWX46199", cartype="Convertible", make="BMW", model="Z4 sDrive30i", year=2022, seats=2, ppd=78, mpg=28, mileage=21199, location="Charlotte", image="bmw_z4_2022.jpg"),
        Car(vin="1G1Y13D78J5105603", cartype="Convertible", make="Chevrolet", model="Corvette Grand Sport LT3", year=2018, seats=2, ppd=83, mpg=24, mileage=60728, location="Durham", image="chev_grand_2018.jpg"),
        Car(vin="WDDWK6Eb2KF806705", cartype="Convertible", make="Mercedes-Benz", model="C-Class AMG C 43", year=2019, seats=2, ppd=69, mpg=23, mileage=13527, location="Wilmington", image="mercedes_amg_2019.jpg"),
        Car(vin="WAUCGAFH3AN014858", cartype="Convertible", make="Audi", model="A5 45 Premium", year="2021", seats=4, ppd=88, mpg=21, mileage=4265, location="Raleigh", image="audi_convert_2021.jpg"),
        Car(vin="1FATP8FF1N5120389", cartype="Convertible", make="Ford", model="Mustang GT Premium", year=2022, seats=4, ppd=85, mpg=22, mileage=13367, location="Asheville", image="ford_gt_convert_2022.jpg"),
        Car(vin="HR768GNSUH5102245", cartype="Convertible", make="Jaguar", model="F-type", year=2022, seats=2, ppd=109, mpg=20, mileage=9232, location="Durham", image="jag_convert_2022.jpg"),
        #Wagon
        Car(vin="KNDJ334AU1M7126N8", cartype="Wagon", make="Kia", model="Soul EX", year=2021, seats=5, ppd=65, mpg=30, mileage=20567, location="Charlotte", image="kia_EX_2021.jpg"),
        Car(vin="4S4BTAFC3M3121300", cartype="Wagon", make="Subaru", model="Outback Premium", year=2021, seats=5, ppd=68, mpg=28, mileage=26988, location="Boone", image="sub_outback_prem_2021.jpg"),
        Car(vin="YVA422NL8M1134998", cartype="Wagon", make="Volvo", model="V90 T6", year=2021, seats=5, ppd=70, mpg=25, mileage=23075, location="Wilmington", image="volvo_2021.jpg"),
        Car(vin="KNDJN2A24J7577222", cartype="Wagon", make="Kia", model="Soul Base", year=2018, seats=5, ppd=55, mpg=28, mileage=19934, location="Asheville", image="kia_base_2018.jpg"),
        Car(vin="4S4T8H1130NFTL022", cartype="Wagon", make="Subaru", model="Outback Premium", year=2021, seats=5, ppd=73, mpg=31, mileage=61902, location="Durham", image="sub_outback_2021.jpg"),
        Car(vin="4S4BTGPD1N3148080", cartype="Wagon", make="Subaru", model="Outback Touring XT", year=2022, seats=5, ppd=80, mpg=27, mileage=15172, location="Raleigh", image="sub_touring_2022.jpg"),
        Car(vin="KNDJ23AU4M7768938", cartype="Wagon", make="Kia", model="Soul LX", year=2021, seats=5, ppd=63, mpg=26, mileage=34928, location="Raleigh", image="kia_lx.jpg"),
        Car(vin="WP0CB2A9XCSH90N54", cartype="Wagon", make="Kia", model="Soul GT-Line", year=2022, seats=5, ppd=57, mpg=32, mileage=28754, location="Greenville", image="kia_GT_2022.jpg"),
        Car(vin="4S0114D79N0128855", cartype="Wagon", make="Subaru", model="Outback Touring XT", year=2021, seats=5, ppd=79, mpg=26, mileage=23734, location="Boone", image="sub_touring_2021.jpg"),
        Car(vin="4S4BENCT9011J4301", cartype="Wagon", make="Subaru", model="Outback 3.6R Limited", year=2019, seats=5, ppd=68, mpg=25, mileage=60023, location="Charlotte", image="sub_3.6r_2019.jpg"),
        Car(vin="43ANB3401J3749N02", cartype="Wagon", make="Subaru", model="Impreza Sport", year=2018, seats=5, ppd=58, mpg=28, mileage=100728, location="Durham", image="sub_impreza_2018.jpg"),
        Car(vin="KNDJP3A52J7094321", cartype="Wagon", make="Kia", model="Soul+", year=2018, seats=5, ppd=50, mpg=27, mileage=84527, location="Wilmington", image="kia_soul+_2018.jpg"),
        Car(vin="4SN02J7782K03L123", cartype="Wagon", make="Subaru", model="Outback", year="2022", seats=5, ppd=72, mpg=28, mileage=14265, location="Raleigh", image="sub_outback_2022.jpg"),
        Car(vin="WMLWNK5CLH2E32112", cartype="Wagon", make="Mini Cooper", model="Clubman", year=2017, seats=5, ppd=85, mpg=53, mileage=63367, location="Asheville", image="mini_coop_clubman.jpg"),
        Car(vin="4S2NCT8L0021NM325", cartype="Wagon", make="Subaru", model="Outback Onyx Edition XT", year=2023, seats=5, ppd=73, mpg=26, mileage=1232, location="Durham", image="sub_onyx_2023.jpg"),
        #Hatchback Cars
        Car(vin="KNAFK5A88H5719594", cartype="Hatchback", make="Kia", model="Forte5 LX", year=2017, seats=5, ppd=95, mpg=25, mileage=12799, location="Durham", image="hb_kiaForte5.jpg"),
        Car(vin="WAUCBCF57MA006273", cartype="Hatchback", make="Kia", model="Rio", year=2017, seats=5, ppd=67, mpg=25, mileage=67092, location="Raleigh", image="hb_kiaRio.jpg"),
        Car(vin="SHHFK7H58HU233486", cartype="Hatchback", make="Honda", model="Civic EX", year=2017, seats=5, ppd=88, mpg=31, mileage=89592, location="Boone", image="hb_hondaCivic.jpg"),
        Car(vin="ML32A3HJ1KH008894", cartype="Hatchback", make="Mitsubishi", model="Mirage ES", year=2019, seats=5, ppd=83, mpg=36, mileage=56050, location="Charlotte", image="hb_mitsub.jpg"),
        Car(vin="JTNC4MBE3M3116049", cartype="Hatchback", make="Toyota", model="Corolla XSE", year=2021, seats=5, ppd=74, mpg=30, mileage=33401, location="Wilmington", image="hb_toyotaCorolla.jpg"),
        Car(vin="19XFL1H79NE012896", cartype="Hatchback", make="Honda", model="Civic EXL", year=2022, seats=5, ppd=96, mpg=30, mileage=21799, location="Asheville", image="hb_hondaEXL.jpg"),
        Car(vin="WMW73DH03P2T40658", cartype="Hatchback", make="Mini Cooper", model="John Cooper Works", year=2023, seats=4, ppd=83, mpg=25, mileage=7008, location="Durham", image="hb_mini.jpg"),
        Car(vin="JM1BPAJL0M1337948", cartype="Hatchback", make="Mazda", model="Mazade3 S", year=2021, seats=5, ppd=78, mpg=26, mileage=28200, location="Wilmington", image="hb_mazada3.jpg"),
        Car(vin="3VWYT7AU0FM032499", cartype="Hatchback", make="Volkswagen", model="GTI S", year=2015, seats=5, ppd=90, mpg=25, mileage=119845, location="Greenville", image="hb_VW.jpg"),
        Car(vin="JM1BPBJY1P1604021", cartype="Hatchback", make="Mazda", model="Mazda3 Turbo", year=2023, seats=5, ppd=85, mpg=23, mileage=9405, location="Greenville", image="hb_mazdaTurbo.jpg"),
        Car(vin="3HGGK5H88FM728818", cartype="Hatchback", make="Honda", model="Fit EX", year=2015, seats=5, ppd=101, mpg=32, mileage=93968, location="Boone", image="hb_hondaFit.jpg"),
        Car(vin="19XFL2H81NE000532", cartype="Hatchback", make="Honda", model="Civic Sport", year=2022, seats=5, ppd=91, mpg=29, mileage=17625, location="Raleigh", image="hb_hondaCivSport.jpg"),
        Car(vin="SHHFK7H90JU233202", cartype="Hatchback", make="Honda", model="Civic Sport Touring", year=2018, seats=5, ppd=72, mpg=31, mileage=95548, location="Charlotte", image="hb_hondaTouring.jpg"),
        Car(vin="3FADP4TJ1GM170938", cartype="Hatchback", make="Ford", model="Fiesta S", year=2016, seats=5, ppd=88, mpg=27, mileage=98127, location="Raleigh", image="hb_fiesta.jpg"),
        Car(vin="WBY1Z4C50EV274347", cartype="Hatchback", make="BMW", model="i3 Range Extender", year=2014, seats=5, ppd=97, mpg=137, mileage=77471, location="Raleigh", image="hb_bmw.jpg"),
        #Vans
        Car(vin="1GCWGBFP8P1103AA7", cartype="Van", make="Chevrolet", model="Express 2500", year=2023, seats=12, ppd=85, mpg=14, mileage=3046, location="Raleigh", image="van_chevExpress.jpg"),
        Car(vin="H1FTYR1YG9GKA1AA7", cartype="Van", make="Honda", model="Odyssey EX L", year=2022, seats=7, ppd=90, mpg=24, mileage=19209, location="Charlotte", image="van_odysseyEXL.jpg"),
        Car(vin="1FTNR1CM4FKA60AA2", cartype="Van", make="Dodge", model="Grand Caravan SE", year=2019, seats=7, ppd=96, mpg=24, mileage=180591, location="Wilmington", image="van_grand.jpg"),
        Car(vin="3C6LRVBG8ME525AA6", cartype="Van", make="Honda", model="Odyssey LX", year=2019, seats=7, ppd=105, mpg=18, mileage=75675, location="Durham", image="van_odysseyLX.jpg"),
        Car(vin="WD4PF0CD6KP026AA5", cartype="Van", make="Mercedes-Benz", model="Sprinter 2500", year=2019, seats=12, ppd=94, mpg=18, mileage=9730, location="Asheville", image="van_sprinter2500.jpg"),
        Car(vin="W1XV0FEYXM3918AA4", cartype="Van", make="Mercedes-Benz", model="Metris", year=2021, seats=7, ppd=82, mpg=18, mileage=20308, location="Greenville", image="van_metris.jpg"),
        Car(vin="1FTBW9CGXLKA67AA6", cartype="Van", make="Honda", model="Odyssey Elite", year=2020, seats=7, ppd=72, mpg=24, mileage=90265, location="Boone", image="van_odysseyElite.jpg"),
        Car(vin="1FTBW9CGXLKA67BA6", cartype="Van", make="Toyota", model="Sienna XSE", year=2022, seats=7, ppd=90, mpg=20, mileage=180995, location="Durham", image="van_sienna.jpg"),
        Car(vin="5BZAF0AA0LN852AA9", cartype="Van", make="Nissan", model="NV 3500HD SL", year=2020, seats=12, ppd=110, mpg=11, mileage=92636, location="Asheville", image="van_3500.jpg"),
        Car(vin="1FBZX2YG4GKA22AA4", cartype="Van", make="Ford", model="Transit XLT", year=2016, seats=12, ppd=83, mpg=22, mileage=69320, location="Charlotte", image="van_fordTrans.jpg"),
        Car(vin="1FTYR2CMXKKA14AA4", cartype="Van", make="Ford", model="Transit Base", year=2019, seats=15, ppd=99, mpg=15, mileage=11137, location="Durham", image="van_fordTransBase.jpg"),
        Car(vin="WD3PE7CC0C5718AA1", cartype="Van", make="Kia", model="Carnival SX Prestige", year=2022, seats=7, ppd=70, mpg=22, mileage=17363, location="Greenville", image="van_carnPrestige.jpg"),
        Car(vin="1FTBW1YK7PKA57AA4", cartype="Van", make="Kia", model="Carnival LX", year=2023, seats=7, ppd=95, mpg=23, mileage=321, location="Boone", image="van_kia.jpg"),
        Car(vin="3C6ERVDG5ME500AA1", cartype="Van", make="Honda", model="Odyssey Touring", year=2022, seats=7, ppd=88, mpg=24, mileage=12738, location="Wilmington", image="van_touring.jpg"),
        Car(vin="1N6AF0LY1DN106AA9", cartype="Van", make="Chrysler", model="Pacifica Touring-L", year=2022, seats=7, ppd=91, mpg=25, mileage=41470, location="Charlotte", image="van_chrysler.jpg")
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
    confirm_password = request.form.get('confirm_password')

    # Check if passwords match
    if password != confirm_password:
        flash('Passwords do not match. Please try again.', 'error')
        return render_template('login.html', create_account_error=True, **request.form)

    # Check if user with this email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already in use.', 'error')
        return render_template('login.html', create_account_error=True, **request.form)

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
    return render_template('faq.html', user=current_user)

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch data for dropdowns
    cities = Car.query.with_entities(Car.location).distinct().all()
    makes = Car.query.with_entities(Car.make).distinct().all()
    categories = Car.query.with_entities(Car.cartype).distinct().all()

    return render_template('dashboard.html', user=current_user, cities=cities, makes=makes, categories=categories)

@app.route('/browse_cars')
@login_required
def browse_cars():
    city = request.args.get('city', None)
    make = request.args.get('make', None)
    cartype = request.args.get('cartype', None) 
    model = request.args.get('model', None) 
    seats = request.args.get('seats', None)
    max_ppd = request.args.get('max_ppd', None)
    sort_option = request.args.get('sort', 'ppd_asc')

    cities = Car.query.with_entities(Car.location).distinct().all()
    makes = Car.query.with_entities(Car.make).distinct().all()
    categories = Car.query.with_entities(Car.cartype).distinct().all()

    query = Car.query

    if city:
        query = query.filter(Car.location == city)
    if make:
        query = query.filter(Car.make == make)
    if cartype:  
        query = query.filter(Car.cartype == cartype)
    if model: 
        query = query.filter(Car.model == model)
    if seats:
        query = query.filter(Car.seats == seats)
    if max_ppd:
        query = query.filter(Car.ppd <= max_ppd)

    # Sorting logic
    if sort_option == 'ppd_asc':
        query = query.order_by(Car.ppd.asc())
    elif sort_option == 'ppd_desc':
        query = query.order_by(Car.ppd.desc())

    cars = query.all()

    # Loop to determine availability
    today = date.today()
    for car in cars:
        active_bookings = Booking.query.filter(
            Booking.car_id == car.vin,
            Booking.start_date <= today,
            Booking.end_date >= today
        ).all()

        car.available = len(active_bookings) == 0

        # Calculate end date for the first active booking (if any)
        car.end_date = None  # Initialize end_date to None if no active bookings
        if active_bookings:
            car.end_date = active_bookings[0].end_date

   
    if len(cars) == 0:
        return render_template('no_cars_found.html')
    else:
        return render_template('browse_cars.html',
                            cars=cars,
                            category=cartype,
                            user=current_user,
                            cities=cities,
                            makes=makes,
                            categories=categories)


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
        
        # Check if the dates are valid
        # if start_date >= end_date or start_date < date.today():
            #flash('Invalid date range.', 'error')
            #return render_template('book_car.html', car=car, user=current_user)

        overlapping_booking = Booking.query.filter(
            and_(
                Booking.car_id == car_vin,
                or_(
                    and_(Booking.start_date <= start_date, Booking.end_date >= start_date),
                    and_(Booking.start_date <= end_date, Booking.end_date >= end_date),
                    and_(Booking.start_date >= start_date, Booking.end_date <= end_date),
                )
            )
        ).first()

        if overlapping_booking:
            flash('Selected dates overlap with a existing booking. Please choose different dates.', 'error')
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
       # After booking is successful
        msg = Message("Car Reservation Confirmation",
                      recipients=[current_user.email])
        msg.body = f"Dear {current_user.first_name},\n\n" \
                   f"You have successfully booked the {car.make} {car.model} from {start_date} to {end_date}.\n" \
                   f"Total cost: ${total_cost}\n\n" \
                   "Thank you for choosing our service."
        mail.send(msg)

        flash(f'Car booked successfully for {total_days} days. Total cost: ${total_cost}', 'success')
        return redirect(url_for('current_reservations'))

    return render_template('book_car.html', car=car, user=current_user)

#@app.route('/api/cars')
#@login_required
#def api_cars():
    #cars = Car.query.all()
    #car_data = [{"vin": car.vin, "make": car.make, "model": car.model, "location": car.location} for car in cars]
    #return jsonify(car_data)    

@app.route('/current_reservations')
@login_required
def current_reservations():
    user_id = current_user.id
    reservations = Booking.query.filter_by(user_id=user_id).all()
    today = datetime.today().date()

    return render_template('current_reservations.html', reservations=reservations, today=today, user=current_user)

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
