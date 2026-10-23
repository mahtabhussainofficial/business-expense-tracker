from flask import Flask, render_template, request, redirect, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from datetime import datetime
import json
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "super_secret_key"

# 🗄️ Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# 🏢 Company Table (Update: Ab yahan business_type save hoga)
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(50), default='general') # NAYA: 'general' ya 'restaurant'
    users = db.relationship('User', backref='company', lazy=True)
    expenses = db.relationship('Expense', backref='company', lazy=True)

# 👤 User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin')  # 'admin' ya 'staff'
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

# 💰 Expense Table
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    trans_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# 📧 --- EMAIL SENDER FUNCTION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "mahtabhussainofficial@gmail.com"
SENDER_PASSWORD = "kguz ymjn fkca qopt"

def send_login_alert(user_name, user_email):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Security Alert: New Login"
        msg["From"] = SENDER_EMAIL
        msg["To"] = user_email
        html_content = f"<h3>Hello {user_name},</h3><p>New login detected to your Expense Tracker account.</p>"
        msg.attach(MIMEText(html_content, "html"))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, user_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Email failed: {e}")

# --- ROUTES ---

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
        
    company_id = session['company_id']
    
    # Check if company is general or restaurant
    current_company = Company.query.get(company_id)
    b_type = current_company.business_type if current_company else 'general'

    company_expenses = Expense.query.filter_by(company_id=company_id).order_by(Expense.id.desc()).all()
    
    total_income = sum(t.amount for t in company_expenses if t.trans_type == 'Income')
    total_expense = sum(t.amount for t in company_expenses if t.trans_type == 'Expense')
    balance = total_income - total_expense

    # Chart logic
    category_totals = {}
    for t in company_expenses:
        if t.trans_type == 'Expense':
            category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

    chart_labels = list(category_totals.keys())
    chart_values = list(category_totals.values())

    # --- DYNAMIC DASHBOARD ROUTING ---
    if b_type == 'restaurant':
        # Restaurant dashboard will have different UI
        return render_template('restaurant_dashboard.html', 
                               transactions=company_expenses, 
                               balance=balance, 
                               income=total_income, 
                               expense=total_expense,
                               user_name=session['user_name'],
                               chart_labels=json.dumps(chart_labels),
                               chart_values=json.dumps(chart_values))
    else:
        # Normal Dashboard
        return render_template('index.html', 
                               transactions=company_expenses, 
                               balance=balance, 
                               income=total_income, 
                               expense=total_expense,
                               user_name=session['user_name'],
                               chart_labels=json.dumps(chart_labels),
                               chart_values=json.dumps(chart_values))

# --- NAYA: MODULE STORE ROUTE ---
@app.route('/modules')
def modules():
    if 'user_id' not in session:
        return redirect('/login')
    # Yahan user ko premium modules dikhayenge
    return render_template('modules.html')
@app.route('/deactivate_restaurant')
def deactivate_restaurant():
    if 'user_id' not in session: 
        return redirect('/login')
    
    company = Company.query.get(session['company_id'])
    if company:
        company.business_type = 'general'
        db.session.commit()
        flash("Switched back to General Dashboard!")
    
    return redirect('/')
# --- NAYA: SWITCH TO RESTAURANT ROUTE ---
@app.route('/activate_restaurant')
def activate_restaurant():
    if 'user_id' not in session: return redirect('/login')
    
    if session.get('role') != 'admin':
        flash("Only Admin can upgrade to Restaurant Mode.")
        return redirect('/')

    company = Company.query.get(session['company_id'])
    if company:
        company.business_type = 'restaurant'
        db.session.commit()
        flash("Restaurant Mode Activated Successfully!")
    
    return redirect('/')

@app.route('/add', methods=['POST'])
def add_transaction():
    if 'user_id' not in session: return redirect('/login')
    
    date_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
    new_expense = Expense(
        user_id=session['user_id'],
        company_id=session['company_id'],
        trans_type=request.form['type'],
        amount=float(request.form['amount']),
        category=request.form['category'],
        date=date_str
    )
    db.session.add(new_expense)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:trans_id>')
def delete_transaction(trans_id):
    if 'user_id' not in session: return redirect('/login')
    
    expense_to_delete = Expense.query.get_or_404(trans_id)
    
    if session['role'] == 'admin' and expense_to_delete.company_id == session['company_id']:
        db.session.delete(expense_to_delete)
        db.session.commit()
    elif expense_to_delete.user_id == session['user_id']:
        db.session.delete(expense_to_delete)
        db.session.commit()
        
    return redirect('/')

@app.route('/reset')
def reset_data():
    if 'user_id' not in session: return redirect('/login')
    
    if session['role'] == 'admin':
        Expense.query.filter_by(company_id=session['company_id']).delete()
        db.session.commit()
    else:
        flash("Action Denied: Only Admin can reset company data!")
        
    return redirect('/')

@app.route('/export_csv')
def export_csv():
    if 'user_id' not in session:
        return redirect('/login')
        
    company_id = session['company_id']
    expenses = Expense.query.filter_by(company_id=company_id).order_by(Expense.id.desc()).all()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Transaction ID', 'Type', 'Category', 'Amount (PKR)', 'Date', 'Logged By User ID'])
    
    for exp in expenses:
        cw.writerow([exp.id, exp.trans_type, exp.category, exp.amount, exp.date, exp.user_id])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=company_expense_report.csv"
    output.headers["Content-Type"] = "text/csv"
    return output

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        company_name = request.form.get('company_name', 'My Business') 
        new_company = Company(name=company_name)
        db.session.add(new_company)
        db.session.commit()
        
        hashed_password = generate_password_hash(request.form['password'])
        new_user = User(
            name=request.form['name'], 
            email=request.form['email'], 
            password=hashed_password,
            role='admin',
            company_id=new_company.id
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash("Company and Admin Account Created!")
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['company_id'] = user.company_id
            session['role'] = user.role
            
            threading.Thread(target=send_login_alert, args=(user.name, user.email)).start()
            return redirect('/')
        else:
            flash("Invalid Credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Access Denied: Only Admins can add staff.")
        return redirect('/')
        
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])
        new_staff = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_password,
            role='staff',
            company_id=session['company_id']
        )
        db.session.add(new_staff)
        db.session.commit()
        
        return redirect('/')
        
    return render_template('add_staff.html')

if __name__ == '__main__':
    app.run(debug=True)