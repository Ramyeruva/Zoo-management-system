import datetime
from datetime import date, timedelta
import os
import random

from bson import ObjectId
from flask import Flask, request, render_template, session, redirect
import pymongo
my_collections = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_collections['zoo_management']
admin_col = my_db['Admin']
doctor_col = my_db['Doctor']
customer_col = my_db['Customer']
guardian_col = my_db['Guardian']
animal_food_col = my_db['Animal_Food']
animal_col = my_db['Animal']
visitor_col = my_db['Visitor']
doctor_request_col = my_db['Doctor_request']
tickets_col = my_db['Tickets']
ticket_booking_col = my_db['Ticket_booking']


app = Flask(__name__)
app.secret_key = "zoo"


App_Root = os.path.dirname(__file__)
App_Root = App_Root + "/static"


if admin_col.count_documents({}) == 0:
    admin_col.insert_one({"name": "admin", "password": "admin", "role": "admin"})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin_login1", methods=['post'])
def admin_login1():
    name = request.form.get("username")
    password = request.form.get("password")
    query = {"username": name, "password": password}
    admin = admin_col.find_one(query)

    if admin != None:
        session['admin_id'] = str(admin['_id'])
        session['role'] = 'Admin'
        return redirect("/admin_home")
    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/guardian")
def guardian():
    guardians = guardian_col.find()
    return render_template("guardian.html", guardians=guardians)


@app.route("/add_guardian")
def add_guardian():
    return render_template("add_guardian.html")


@app.route("/add_guardian1", methods=['post'])
def add_guardian1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    age = request.form.get("age")
    gender = request.form.get("gender")
    about = request.form.get("about")
    query = {"$or": [{"email": email}, {"phone": phone}]}
    count = guardian_col.count_documents(query)
    if count > 0:
        return render_template("msg.html", message="Duplicate Details", color="bg-danger text-white")
    else:
        query = {"name": name, "email": email, "phone": phone, "password": password, "age": age, "gender": gender, "about": about}
    guardian_col.insert_one(query)
    return redirect("/guardian")


@app.route("/guardian_login")
def guardian_login():
    return render_template("guardian_login.html")


@app.route("/guardian_login1", methods=['post'])
def guardian_login1():
    email = request.form.get('email')
    password = request.form.get('password')
    query = {"email": email, "password": password}
    count = guardian_col.count_documents(query)
    if count > 0:
        guardian = guardian_col.find_one(query)
        session['guardian_id'] = str(guardian['_id'])
        session['role'] = 'Guardian'
        return redirect("/guardian_home")

    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/guardian_home")
def guardian_home():
    return render_template("guardian_home.html")


@app.route("/doctor_login")
def doctor_login():
    return render_template("doctor_login.html")


@app.route("/doctor_login1", methods=['post'])
def doctor_login1():
    email = request.form.get('email')
    password = request.form.get('password')
    query = {"email": email, "password": password}
    count = doctor_col.count_documents(query)
    if count > 0:
        doctor = doctor_col.find_one(query)
        session['doctor_id'] = str(doctor['_id'])
        session['role'] = 'Doctor'
        return redirect("/doctor_home")

    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/doctor_home")
def doctor_home():
    return render_template("doctor_home.html")


@app.route("/doctors")
def doctors():
    doctors = doctor_col.find()
    return render_template("doctors.html", doctors=doctors)


@app.route("/add_doctor")
def add_doctor():
    return render_template("add_doctor.html")


@app.route("/add_doctor1", methods=['post'])
def add_doctor1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    age = request.form.get("age")
    gender = request.form.get("gender")
    qualification = request.form.get("qualification")
    specialization = request.form.get("specialization")
    experience = request.form.get("experience")
    about = request.form.get("about")
    query = {"$or": [{"email": email}, {"phone": phone}]}
    count = doctor_col.count_documents(query)
    if count > 0:
        return render_template("msg.html", message="Duplicate Details", color="bg-danger text-white")
    else:
        query = {"name": name, "email": email, "phone": phone, "password": password, "age": age, "gender": gender, "about": about, "experience": experience, "qualification": qualification, "specialization": specialization}
    doctor_col.insert_one(query)
    return redirect("/doctors")


@app.route("/customer_login")
def customer_login():
    return render_template("customer_login.html")


@app.route("/customer_login1", methods=['post'])
def customer_login1():
    email = request.form.get('email')
    password = request.form.get('password')
    query = {"email": email, "password": password}
    count = customer_col.count_documents(query)
    if count > 0:
        customer = customer_col.find_one(query)
        session['customer_id'] = str(customer['_id'])
        session['role'] = 'Customer'
        return redirect("/customer_home")

    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/customer_home")
def customer_home():
    return render_template("customer_home.html")


@app.route("/customer_registration")
def customer_registration():
    return render_template("customer_registration.html")


@app.route("/customer_registration1", methods=['post'])
def customer_registration1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    age = request.form.get("age")
    gender = request.form.get("gender")
    query = {"$or": [{"email": email}, {"phone": phone}]}
    count = customer_col.count_documents(query)
    if count > 0:
        return render_template("msg.html", message="Duplicate Details", color="bg-danger text-white")
    else:
        query = {"name": name, "email": email, "phone": phone, "password": password, "age": age, "gender": gender}
    customer_col.insert_one(query)
    return redirect("/customer_login")


@app.route("/add_animals")
def add_animals():
    return render_template("add_animals.html")


@app.route("/add_animal1", methods=['post'])
def add_animal1():
    guardian_id = session['guardian_id']
    animal_name = request.form.get("animal_name")
    animal_type = request.form.get("animal_type")
    weight = request.form.get("weight")
    picture = request.files.get('picture')
    path = App_Root + "/pictures/" + picture.filename
    picture.save(path)

    age = request.form.get("age")
    gender = request.form.get("gender")
    about = request.form.get("about")
    query = {"guardian_id": ObjectId(guardian_id), "animal_name": animal_name, "animal_type": animal_type, "weight": weight, "picture": picture.filename, "age": age, "gender": gender, "about": about}
    animal_col.insert_one(query)
    return redirect("/view_animals")


@app.route("/view_animals")
def view_animals():
    if session['role'] == "Admin" or session['role'] == "Customer":
        animals = animal_col.find()
        animal_ids = []
        for animal in animals:
            animal_ids.append({"_id": animal['_id']})
        query = {"$or": animal_ids}
    elif session['role'] == "Guardian":
        query = {"guardian_id": ObjectId(session['guardian_id'])}
    animals = animal_col.find(query)
    return render_template("view_animals.html", animals=animals)


@app.route("/add_food")
def add_food():
    animal_id = request.args.get("animal_id")
    return render_template("add_food.html", animal_id=animal_id)


@app.route("/add_food1", methods=['post'])
def add_food1():
    animal_id = request.form.get("animal_id")
    food_name = request.form.get("food_name")
    food_time = request.form.get("food_time")

    query = {"animal_id": ObjectId(animal_id), "food_name": food_name, "food_time": food_time}
    animal_food_col.insert_one(query)
    return redirect("/view_food")


@app.route("/view_food")
def view_food():
    animal_id = request.args.get("animal_id")
    query = {"animal_id": ObjectId(animal_id)}
    animal_foods = animal_food_col.find(query)
    return render_template("view_food.html", animal_foods=animal_foods, get_animal_id=get_animal_id, formate_time=formate_time)


def get_animal_id(animal_id):
    query = {"_id": ObjectId(animal_id)}
    animal = animal_col.find_one(query)
    return animal


def get_doctor_id(doctor_id):
    query = {"_id": ObjectId(doctor_id)}
    doctor = doctor_col.find_one(query)
    return doctor


@app.route("/send_doctor_request")
def send_doctor_request():
    animal_id = request.args.get("animal_id")
    doctors = doctor_col.find()
    return render_template("send_doctor_request.html", animal_id=animal_id, doctors=doctors)


@app.route("/send_doctor_request1", methods=['post'])
def send_doctor_request1():
    doctor_id = request.form.get("doctor_id")
    animal_id = request.form.get("animal_id")
    cause = request.form.get("cause")
    request_date = datetime.datetime.now()
    status = "Request Sent to Doctor"
    query = {"doctor_id": ObjectId(doctor_id), "animal_id": ObjectId(animal_id), "cause": cause, "request_date": request_date, "status": status}
    doctor_request_col.insert_one(query)
    return render_template("msg.html", message="Send Request ", color="bg-success text-white")


@app.route("/view_doctor_requests")
def view_doctor_requests():
    animal_id = request.args.get("animal_id")
    if session['role'] == "Guardian" or session['role'] == "Admin":
        query = {"animal_id": ObjectId(animal_id)}
    elif session['role'] == "Doctor":
        query = {"doctor_id": ObjectId(session['doctor_id'])}
    doctor_requests = doctor_request_col.find(query)
    return render_template("view_doctor_requests.html", get_doctor_id=get_doctor_id, doctor_requests=doctor_requests, get_animal_id=get_animal_id)


@app.route("/view_doctor")
def view_doctor():
    doctor_id = request.args.get("doctor_id")
    query = {"_id": ObjectId(doctor_id)}
    doctor = doctor_col.find_one(query)
    return render_template("view_doctor.html", doctor=doctor)


@app.route("/add_treatment")
def add_treatment():
    animal_id = request.args.get("animal_id")
    doctor_request_id = request.args.get("doctor_request_id")
    return render_template("add_treatment.html", doctor_request_id=doctor_request_id, animal_id=animal_id)


@app.route("/add_treatment1", methods=['post'])
def add_treatment1():
    doctor_request_id = request.form.get("doctor_request_id")
    treatment = request.form.get("treatment")
    treatment_date = datetime.datetime.now()
    status = "Treatment Done"
    query = {"_id": ObjectId(doctor_request_id)}
    query1 = {"$set": {"treatment": treatment, "treatment_date": treatment_date, "status": status}}
    doctor_request_col.update_one(query, query1)
    return render_template("msg.html", message="Treatment Done", color="bg-success text-white")


@app.route("/view_treatments")
def view_treatments():
    animal_id = request.args.get("animal_id")
    if session['role'] == "Guardian" or session['role'] == "Admin":
        query = {"animal_id": ObjectId(animal_id)}
    elif session['role'] == "Doctor":
        query = {"doctor_id": ObjectId(session['doctor_id'])}
    doctor_requests = doctor_request_col.find(query)
    return render_template("view_treatments.html", get_doctor_id=get_doctor_id, doctor_requests=doctor_requests, get_animal_id=get_animal_id)


@app.route("/tickets")
def tickets():
    tickets = tickets_col.find()
    return render_template("tickets.html", tickets=tickets, get_ticket_booking_id=get_ticket_booking_id)


@app.route("/add_ticket")
def add_ticket():
    return render_template("add_ticket.html")


@app.route("/add_ticket1", methods=['post'])
def add_ticket1():
    ticket_title = request.form.get("ticket_title")
    available_tickets = request.form.get("available_tickets")
    price_per_children = request.form.get("price_per_children")
    price_per_adult = request.form.get("price_per_adult")
    query = {"ticket_title": ticket_title, "available_tickets": available_tickets, "price_per_children": price_per_children, "price_per_adult": price_per_adult}
    tickets_col.insert_one(query)
    return redirect("/tickets")


@app.route("/book_tickets")
def book_tickets():
    ticket_id = request.args.get("ticket_id")
    return render_template("book_tickets.html", ticket_id=ticket_id)


@app.route("/book_tickets1", methods=['post'])
def book_tickets1():
    ticket_id = request.form.get("ticket_id")
    query = {"_id": ObjectId(ticket_id)}
    ticket = tickets_col.find_one(query)
    customer_id = session['customer_id']
    no_of_bookings = request.form.get("no_of_bookings")
    children_count = request.form.get("children_count")
    adult_count = request.form.get("adult_count")
    price_per_children = ticket['price_per_children']
    price_per_adult = ticket['price_per_adult']

    children_price = int(price_per_children) * int(children_count)
    adult_price = int(price_per_adult) * int(adult_count)
    total_price = int(children_price) + int(adult_price)
    date = datetime.datetime.now()
    status = "Ticket Booked by Customer"
    query = {"ticket_id": ObjectId(ticket_id), "customer_id": ObjectId(customer_id), "no_of_bookings": no_of_bookings, "children_count": children_count, "adult_count": adult_count, "total_price": total_price, "date": date, "status": status}
    result = ticket_booking_col.insert_one(query)
    ticket_booking_id = result.inserted_id
    for i in range(1, int(children_count) + 1):
        name = request.form.get("name" + str(i))
        age = request.form.get("age" + str(i))
        query = {"ticket_booking_id": ObjectId(ticket_booking_id), "name": name, "age": age, "visitor_type": "Children"}
        visitor_col.insert_one(query)

    for i in range(1, int(adult_count) + 1):
        name = request.form.get("name" + str(i))
        age = request.form.get("age" + str(i))
        query = {"ticket_booking_id": ObjectId(ticket_booking_id), "name": name, "age": age, "visitor_type": "Adult"}
        visitor_col.insert_one(query)

    return render_template("msg.html", message="Ticket Booked Successfully", color="bg-success text-white")


@app.route("/view_booked_tickets")
def view_tickets():
    ticket_id = request.args.get("ticket_id")
    query = {"ticket_id": ObjectId(ticket_id)}
    bookings = ticket_booking_col.find(query)
    return render_template("view_booked_tickets.html", bookings=bookings, get_ticket_id=get_ticket_id, get_customer_id=get_customer_id)


def get_ticket_id(ticket_id):
    query = {"_id": ObjectId(ticket_id)}
    ticket = tickets_col.find_one(query)
    return ticket


def get_customer_id(customer_id):
    query = {"_id": ObjectId(customer_id)}
    customer = customer_col.find_one(query)
    return customer


def get_ticket_booking_id(ticket_id):
    query = {"ticket_id": ObjectId(ticket_id)}
    booking = ticket_booking_col.find_one(query)
    if booking!=None:
        no_of_bookings = booking['no_of_bookings']
        ticket_id = booking['ticket_id']
        query = {"_id": ObjectId(ticket_id)}
        ticket = tickets_col.find_one(query)
        available_tickets = ticket['available_tickets']
        remaining_tickets = int(available_tickets) - int(no_of_bookings)
    else:
        query = {"_id": ObjectId(ticket_id)}
        ticket = tickets_col.find_one(query)
        available_tickets = ticket['available_tickets']
        remaining_tickets = available_tickets
    return remaining_tickets


@app.route("/view_visitors")
def view_visitors():
    ticket_booking_id = request.args.get("ticket_booking_id")
    query = {"ticket_booking_id": ObjectId(ticket_booking_id)}
    visitors = visitor_col.find(query)
    return render_template("view_visitors.html", visitors=visitors)


@app.route("/pay_amount")
def pay_amount():
    return render_template("pay_amount.html")


@app.route("/pay_amount1", methods=['post'])
def pay_amount1():
    return render_template("msg.html", message="Amount Paid Successfully", color="bg-success text-white")


def formate_time(food_time):
    print(food_time)
    date = datetime.datetime.strptime(str(datetime.datetime.now().date())+" "+food_time,"%Y-%m-%d %H:%M")
    food_time = str(date.strftime("%I"))+":"+str(date.strftime("%M"))+" "+str(date.strftime("%p"))
    print(food_time)
    return food_time


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


app.run(debug=True)