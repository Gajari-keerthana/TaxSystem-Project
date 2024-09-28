from flask import Flask, request,jsonify, render_template, redirect, url_for, session, flash
from models import db, Company, Tax, User
import urllib.parse
from datetime import datetime
from sqlalchemy import func
from flask import flash
from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "1c8463cb0376afe071d51315c70859e027770297df8fdf88e958a456eb2aa470"

# Connecting to Database Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxpaymenttrackingsys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables if they do not exist
with app.app_context():
    db.create_all()


# Home Screen
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Get All Records with filters
@app.route('/index', methods=['GET'])
def index():
    #check if a user_id is stored in session which means the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login')) # Redirect to login if not authenticated
    due_date_filter = request.args.get('due_date')

    # Fetch tax records based on due date filter
    if due_date_filter:
        taxes = Tax.query.filter(Tax.due_date == due_date_filter).all()

        # Calculate total amount and tax due only on filtered results
        total_amount = sum(tax.amount for tax in taxes)
        tax_rate = 0.06
        tax_due = total_amount * tax_rate
    else:
        taxes = Tax.query.all()

        # Calculate total amount and tax due on all records if no filter applied
        total_amount = db.session.query(func.sum(Tax.amount)).scalar() or 0
        tax_rate = 0.06
        tax_due = total_amount * tax_rate

    return render_template('index.html', taxes=taxes, total_amount=total_amount, tax_rate=tax_rate, tax_due=tax_due)

# Create Record
@app.route('/add', methods=['GET','POST'])
def add_record():
    if request.method == 'POST':
        company_name = request.form['company']
        amount = request.form['amount']
        payment_date_str = request.form['payment_date']
        status = request.form['status']
        due_date_str = request.form['due_date']

        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
            db.session.commit()

        # Set payment_date to None if not provided
        payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d').date() if payment_date_str else None
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

        new_tax = Tax(company=company, amount=amount, payment_date=payment_date, status=status, due_date=due_date)
        db.session.add(new_tax)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add_record.html')

# Edit Record
@app.route('/edit/<int:tax_id>', methods=['GET', 'POST'])
def edit_record(tax_id):
    tax = Tax.query.get_or_404(tax_id)
    if request.method == 'POST':
        tax.company.name = request.form['company']
        tax.amount = request.form['amount']
        tax.status = request.form['status']

        # Handle payment_date and due_date
        payment_date = request.form.get('payment_date', None)
        due_date = request.form.get('due_date', None)

        # Convert date strings to datetime objects
        tax.payment_date = datetime.strptime(payment_date, "%Y-%m-%d") if payment_date else None
        tax.due_date = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_record.html', tax=tax)

# Delete Record
@app.route('/delete/<int:tax_id>', methods=['POST'])
def delete_record(tax_id):
    tax = Tax.query.get_or_404(tax_id)
    db.session.delete(tax)
    db.session.commit()
    return redirect(url_for('index'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # This is where you query your database for the user
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Storing user's ID in session after successful login
            session['user_id'] = user.id
            return redirect(url_for('index')) # Redirect to the index page if login is successful
        else:
            flash('Invalid username or password') # Send an error message to the next page

    return render_template('login.html')

#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password').strip()  #Remove leading/trailing spaces
        confirm_password = request.form.get('confirm_password', '').strip()  # Default to empty string if not found

        #Debugging output to console
        print(f"Password: '{password}'")
        print(f"Confirm Password: '{confirm_password}'")

        # Check if password match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.')
            return render_template('register.html', username=username, email=email)
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.')
            return render_template('register.html', username=username, email=email)
        
        #Hash the password
        hashed_password = generate_password_hash(password)

        # Create new user with hashed password
        new_user = User(username=username, email=email, password_hash=hashed_password)

        # Add new user to the database
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('User created successfully. Please log in.')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('This email already exists. Please use a different email.')
            return render_template('register.html', username=username) 

    # If it's a Get request, just render the template
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)

