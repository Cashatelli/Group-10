'''engine = create_engine("sqlite://users.db", echo = true)
Base.metadata.create_all(bind=engine)

class Car(db.Model):
__tablename__ = "cars"

 vin = db.Column(db.String(50), unique = True, primary_key = True)
 cartype = db.Column(db.String(50))
 
 make = db.Column(db.String(50))
 model = db.Column(db.String(50))
 year = db.Column(db.Integer)
 
 seats = db.Column(db.Integer)
 ppd = db.Column(db.Integer)
 mpg = db.Column(db.Integer)
 mileage = db.Column(db.Integer)
 
 current_customer_cid = db.Column(db.integer, unique = True, default = null)
 location = db.Column(db.String(100))
 Image = db.Column(db.String(500))

Session = sessionmaker(bind = engine)
session = Session()
c1 = Car("1FTEW1EG6HFC30991", "Pickup", "Ford", "F-150", 2017, 4, 95, 20, 80014, null, "Winterville", "img")
c2 = Car("1FT7W2B64JEB65645", "Pickup", "Ford", "F-250", 2018, 4, 102, 21, 99103, null "Winterville", "img")
c3 = Car("1FT8W2BT9NEC70388", "Pickup", "Ford", "F-250", 2022, 4, 155, 24, 89041, null "Raleigh", "img")
c4 = Car("1C6HJTFG7NL119666", "Pickup", "Jeep", "Gladiator", 2022, 4, 165, 20, 20100, null, "Winterville", "img")
c5 = Car("1GC4YUEY6MF190132", "Pickup", "Chevrolet", "Silverado", 2021, 4, 120, 21, 89095, null, "Raleigh", "img")
c6 = Car("1C6RREFT6MN543610", "Pickup", "Ram", "1500", 2021, 4, 98, 19, 98874, null, "Winterville", "img")
c7 = Car("5FPYK3F72KB028445", "Pickup", "Honda", "Ridgeline", 2019, 4, 115, 22, 68798, null, "Raleigh", "img")
c8 = Car("3C6RR6LT3JG146144", "Pickup", "Ram", "1500", 2018, 4, 88, 19, 124794, null, "Charlotte", "img")
c9 = Car("1C6SRFBTXKN733890", "Pickup", "Ram", "1500", 2019, 4, 95, 18, 72380, null, "Raleigh", "img")
c10 = Car("5NTJEDAF7NH011122", "Pickup", "Hyundai", "Santa_Cruz", 2022, 4, 143, 24, 13159, null, "Charlotte", "img")
c11 = Car("1FTEW1EGXJFE55694", "Pickup", "Ford", "F-150", 2018, 4, 118, 19, 86410, null, "Charlotte", "img")
c12 = Car("1GTN1LEC4GZ146768", "Pickup", "GMC", "Sierra_1500", 2016, 2, 79, 20, 118713, null, "Charlotte", "img")
c13 = Car("1GTN1LEC1HZ905958", "Pickup", "GMC", "Sierra_1500", 2017, 2, 75, 20, 101170, null, "Raleigh", "img")
c14 = Car("3C6JR6DT6GG239518", "Pickup", "Ram", "1500", 2016, 2, 94, 19, 49084, null, "Winterville", "img")
c15 = Car("1FTMF1C88GKF91569", "Pickup", "Ford", "F-150", 2016, 2, 90, 21, 97477, null, "Charlotte", "img")

c16 = Car("WBAKB8C51CC964616", "Sedan", "BMW", "7_Series", 2012, 5, 75, 18, 91767, null, "Raleigh", "img")
c17 = Car("1G11B5SA1DF256175", "Sedan", "Chevrolet", "Malibu", 2013, 5, 88, 27, 137018, null, "Charlotte", "img")
c18 = Car("W1KWF8DBXMR642820", "Sedan", "Mercedes-Benz", "C-Class", 2021, 5, 126, 29, 35799, null, "Raleigh", "img")
c19 = Car("7JR102FK9LG045640", "Sedan", "Volvo", "S60", 2020, 5, 110, 29, 36145, null, "Winterville", "img")
c20 = Car("5NPE34AF0KH785469", "Sedan", "Hyundai", "Sonata", 2019, 5, 97, 29, 120714, null, "Charlotte", "img")
c21 = Car("1G6DN5RW3M0110685", "Sedan", "Cadillac", "CT5", 2021, 5, 131, 24, 20698, null, "Winterville", "img")
c22 = Car("19UUB2F39GA012467", "Sedan", "Acura", "TLX", 2016, 5, 83, 28, 127952, null, "Winterville", "img")
c23 = Car("KNAE35LD3N6099133", "Sedan", "Kia", "Stinger", 2022, 5, 103, 27, 32002, null, "Charlotte", "img")
c24 = Car("4T1K61AK9MU614780", "Sedan", "Toyota", "Camry", 2021, 5, 78, 32, 47272, null, "Raleigh", "img")
c25 = Car("3FA6P0HD0LR143456", "Sedan", "Ford", "Fusion", 2020, 5, 91, 28, 40977, null, "Raleigh", "img")
c26 = Car("3KPF54AD3NE448185", "Sedan", "Kia", "Forte", 2022, 5, 99, 35, 11564, null, "Charlotte", "img")
c27 = Car("7JRBR0FM4NG179054", "Sedan", "Volvo", "S60", 2022, 5, 106, 31, 15365, null, "Raleigh", "img")
c28 = Car("KMHLN4AJ0PU047489", "Sedan", "Hyundai", "Elantra", 2023, 5, 114, 51, 10820, null, "Winterville", "img")
c29 = Car("3KPF24AD8ME359039", "Sedan", "Kia", "Forte", 2021, 5, 81, 34, 17850, null, "Winterville", "img")
c30 = Car("5XXGT4L33KG330445", "Sedan", "Kia", "Optima", 2019, 5, 77, 29, 37976, null, "Charlotte", "img")
i = 1 
while(i <= 30)
    session.add(c + i)
    i = i + 1

'''
'''Car(vin="1FT7W2B64JEB65645", cartype="Pickup", make="Ford", model="F-250", year=2018, seats=4, ppd=102, mpg=21, mileage=99103, current_customer_cid=None, location="Winterville", image="F-250_2018.jpg")
        Car(vin="1FT8W2BT9NEC70388", cartype="Pickup", make="Ford", model="F-250", year=2022, seats=4, ppd=155, mpg=24, mileage=89041, current_customer_cid=None, location="Raleigh", image="F-250_2022.jpg"),
        Car(vin="1C6HJTFG7NL119666", cartype="Pickup", make="Jeep", model="Gladiator", year=2022, seats=4, ppd=165, mpg=20, mileage=20100, current_customer_cid=None, location="Winterville", image="jeep_gladiator_2022.jpg"),
        Car(vin="1GC4YUEY6MF190132", cartype="Pickup", make="Chevrolet", model="Silverado", year=2021, seats=4, ppd=120, mpg=21, mileage=89095, current_customer_cid=None, location="Raleigh", image="chevrolet_silverado_2022.jpg"),
        Car(vin="1C6RREFT6MN543610", cartype="Pickup", make="Ram", model="1500", year=2021, seats=4, ppd=98, mpg=19, mileage=98874, current_customer_cid=None, location="Winterville", image="ram_1500_2021.jpg"),
        Car(vin="5FPYK3F72KB028445", cartype="Pickup", make="Honda", model="Ridgeline", year=2019, seats=4, ppd=115, mpg=22, mileage=68798, current_customer_cid=None, location="Raleigh", image="honda_ridgeline_2019.jpg"),
        Car(vin="3C6RR6LT3JG146144", cartype="Pickup", make="Ram", model="1500", year=2018, seats=4, ppd=88, mpg=19, mileage=124794, current_customer_cid=None, location="Charlotte", image="ram_1500_2018.jpg"),
        Car(vin="1C6SRFBTXKN733890", cartype="Pickup", make="Ram", model="1500", year=2019, seats=4, ppd=95, mpg=18, mileage=72380, current_customer_cid=None, location="Raleigh", image="ram_1500_2019.jpg"),   
        Car(vin="5NTJEDAF7NH011122", cartype="Pickup", make="Hyundai", model="Santa_Cruz", year=2022, seats=4, ppd=143, mpg=24, mileage=13159, current_customer_cid=None, location="Charlotte", image="hyundai_santacruz_2022.jpg"),
        Car(vin="1FTEW1EGXJFE55694", cartype="Pickup", make="Ford", model="F-150", year=2018, seats=4, ppd=118, mpg=19, mileage=86410, current_customer_cid=None, location="Charlotte", image="ford_f-150_2018.jpg"),
        Car(vin="1GTN1LEC4GZ146768", cartype="Pickup", make="GMC", model="Sierra_1500", year=2016, seats=2, ppd=79, mpg=20, mileage=118713, current_customer_cid=None, location="Charlotte", image="gmc_serria_2016.jpg"),
        Car(vin="1GTN1LEC1HZ905958", cartype="Pickup", make="GMC", model="Sierra_1500", year=2017, seats=2, ppd=75, mpg=20, mileage=101170, current_customer_cid=None, location="Raleigh", image="gmc_serria_2017.jpg"),
        Car(vin="3C6JR6DT6GG239518", cartype="Pickup", make="Ram", model="1500", year=2016, seats=2, ppd=94, mpg=19, mileage=49084, current_customer_cid=None, location="Winterville", image="ram_1500_2016.jpg"),
        Car(vin="1FTMF1C88GKF91569", cartype="Pickup", make="Ford", model="F-150", year=2016, seats=2, ppd=90, mpg=21, mileage=97477, current_customer_cid=None, location="Charlotte", image="ford_F-150_2016.jpg"),

        Car(vin="WBAKB8C51CC964616", cartype="Sedan", make="BMW", model="7_Series", year=2012, seats=5, ppd=75, mpg=18, mileage=91767, current_customer_cid=None, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="1G11B5SA1DF256175", cartype="Sedan", make="Chevrolet", model="Malibu", year=2013, seats=5, ppd=88, mpg=27, mileage=137018, current_customer_cid=None, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="W1KWF8DBXMR642820", cartype="Sedan", make="Mercedes-Benz", model="C-Class", year=2021, seats=5, ppd=126, mpg=29, mileage=35799, current_customer_cid=None, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="7JR102FK9LG045640", cartype="Sedan", make="Volvo", model="S60", year=2020, seats=5, ppd=110, mpg=29, mileage=36145, current_customer_cid=None, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="5NPE34AF0KH785469", cartype="Sedan", make="Hyundai", model="Sonata", year=2019, seats=5, ppd=97, mpg=29, mileage=120714, current_customer_cid=None, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="1G6DN5RW3M0110685", cartype="Sedan", make="Cadillac", model="CT5", year=2021, seats=5, ppd=131, mpg=24, mileage=20698, current_customer_cid=None, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="19UUB2F39GA012467", cartype="Sedan", make="Acura", model="TLX", year=2016, seats=5, ppd=83, mpg=28, mileage=127952, current_customer_cid=None, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="KNAE35LD3N6099133", cartype="Sedan", make="Kia", model="Stinger", year=2022, seats=5, ppd=103, mpg=27, mileage=32002, current_customer_cid=None, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="4T1K61AK9MU614780", cartype="Sedan", make="Toyota", model="Camry", year=2021, seats=5, ppd=78, mpg=32, mileage=47272, current_customer_cid=None, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="3FA6P0HD0LR143456", cartype="Sedan", make="Ford", model="Fusion", year=2020, seats=5, ppd=91, mpg=28, mileage=40977, current_customer_cid=None, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="3KPF54AD3NE448185", cartype="Sedan", make="Kia", model="Forte", year=2022, seats=5, ppd=99, mpg=35, mileage=11564, current_customer_cid=None, location="Charlotte", image="Sedan_image.jpg"),
        Car(vin="7JRBR0FM4NG179054", cartype="Sedan", make="Volvo", model="S60", year=2022, seats=5, ppd=106, mpg=31, mileage=15365, current_customer_cid=None, location="Raleigh", image="Sedan_image.jpg"),
        Car(vin="KMHLN4AJ0PU047489", cartype="Sedan", make="Hyundai", model="Elantra", year=2023, seats=5, ppd=114, mpg=51, mileage=10820, current_customer_cid=None, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="3KPF24AD8ME359039", cartype="Sedan", make="Kia", model="Forte", year=2021, seats=5, ppd=81, mpg=34, mileage=17850, current_customer_cid=None, location="Winterville", image="Sedan_image.jpg"),
        Car(vin="5XXGT4L33KG330445", cartype="Sedan", make="Kia", model="Optima", year=2019, seats=5, ppd=77, mpg=29, mileage=37976, current_customer_cid=None, location="Charlotte", image="Sedan_image.jpg")
'''