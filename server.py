from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

mysql = MySQLConnector(app,'email_valid')
@app.route('/')
def index():
    query = "SELECT * FROM email"
    # define your query
    email = mysql.query_db(query)
    print email
    return render_template('index.html', all_email=email)

@app.route('/success')
def success():
    # email = request.form['email']
    query = "SELECT * FROM email"
    # define your query
    email = mysql.query_db(query)
    return render_template('success.html', all_email=email)

@app.route('/email', methods=['POST'])
def create():
    error_count = 0
    email = request.form['email']

    if len(email) < 1:
        flash("Email must be longer than 1 character, bruh!")
        error_count += 1
        print "Error Count: ", error_count, " - Email Error"
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
        error_count += 1
        print "Error Count: ",  error_count, " - Email Error"

    if error_count == 0:
        data = {
            'email': email
        }
        query = 'SELECT * from email where email = :email'
        output = mysql.query_db(query, data)
        print output
        if len(output) > 0:
            flash("FAILURE! Email Found In Database!", "error")
        elif len(output) == 0:
            flash("Email added to Database", "success")

            query = "INSERT INTO email (email, created_at) VALUES (:email, NOW())"
            data = {
                     'email': email
                   }
            mysql.query_db(query, data)
            return redirect('/success')

    return redirect('/')
app.run(debug=True)
