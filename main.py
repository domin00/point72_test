from flask import Flask, render_template, redirect, url_for, request
import sqlite3


# -------- DATABASE SECTION ----------
# create database
conn = sqlite3.connect('point72.db')
c = conn.cursor()

# Create Tables
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY,
              first_name TEXT,
              last_name TEXT,
              email TEXT UNIQUE,
              password TEXT,
              age INTEGER,
              country TEXT,
              role TEXT)
              ''')

conn.commit()
print("SQLite table created")
c.close()




# ------------ FLASK LOGIC SECTION -------------
# run flask app
app = Flask(__name__)

# login page route
#   -login authorization
#   -save user_name and user_role for personalization of website responses
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        conn = sqlite3.connect('point72.db')
        c = conn.cursor()
        email = request.form.get('email')
        password = request.form.get('password')
        c.execute("SELECT email, password, role, first_name FROM users WHERE email = ?", (email,))
        valemail = c.fetchone()

        if valemail is None:
          return "No such e-mail and password combination. Please register to log in."

        if valemail[1] == password:
            print("Password is correct.")
            global user_name
            global user_role
            user_name = valemail[3]
            user_role = valemail[2]
            return redirect(url_for('home', user_name=user_name, user_role=user_role))
        else:
            return "E-mail and Password combination is incorrect. Try again."

    return render_template("login.html")

# registration page route
#   -new user creation into the database
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect('point72.db')
        c = conn.cursor()
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        country = request.form.get('country')
        role = request.form.get('type')

        sql = ("INSERT INTO users (first_name, last_name, email, password, age, country, role) VALUES (?, ?, ?, ?, ?, ?, ?)")
        c.execute(sql,(first_name, last_name, email, password, age, country, role))
        conn.commit()
        return redirect('/')

    return render_template("registration.html")

# homw page route
#   -list users
#   -modify users if allowed
#   -filter users
@app.route('/home/<user_name>/<user_role>', methods=['GET', 'POST'])
def home(user_name, user_role):

    # connect to DB for both GET and POST
    conn = sqlite3.connect('point72.db')
    c = conn.cursor()

    # functionality of POST logic below
    if request.method == "POST":

        # ------  filter logic   --------

        # age filter
        if "age_button" in request.form:
            age_from = request.form.get('age_from')
            age_to = request.form.get('age_to')
            print(age_from)
            c.execute('SELECT * FROM users WHERE age BETWEEN ? and ?', (age_from, age_to))
            data = [dict(
             id = row[0],
             first_name = row[1],
             last_name = row[2],
             email = row[3],
             age = row[5],
             country = row[6]
            ) for row in c.fetchall()]
            print(data)



            if user_role == 'admin':
                return render_template("home_admin.html", user_name=user_name, user_role=user_role, data=data)
            if user_role == 'regular':
                return render_template("home_regular.html", user_name=user_name, user_role=user_role, data=data)

        # first name filter
        elif "first_button" in request.form:
            first_name_part = request.form.get('first_name_part')
            print(first_name_part)
            c.execute('SELECT * FROM users WHERE first_name LIKE ?', ('%'+first_name_part+'%',))
            data = [dict(
             id = row[0],
             first_name = row[1],
             last_name = row[2],
             email = row[3],
             age = row[5],
             country = row[6]
            ) for row in c.fetchall()]

            if user_role == 'admin':
                return render_template("home_admin.html", user_name=user_name, user_role=user_role, data=data)
            if user_role == 'regular':
                return render_template("home_regular.html", user_name=user_name, user_role=user_role, data=data)

        # last name filter
        elif "last_button" in request.form:
            last_name_part = request.form.get('last_name_part')
            c.execute('SELECT * FROM users WHERE last_name LIKE ?', ('%'+last_name_part+'%',))
            data = [dict(
             id = row[0],
             first_name = row[1],
             last_name = row[2],
             email = row[3],
             age = row[5],
             country = row[6]
            ) for row in c.fetchall()]

            if user_role == 'admin':
                return render_template("home_admin.html", user_name=user_name, user_role=user_role, data=data)
            if user_role == 'regular':
                return render_template("home_regular.html", user_name=user_name, user_role=user_role, data=data)

        # country filter
        elif "country_button" in request.form:
            country = request.form.get('country')
            c.execute('SELECT * FROM users WHERE country LIKE ?', ('%'+country+'%',))
            data = [dict(
             id = row[0],
             first_name = row[1],
             last_name = row[2],
             email = row[3],
             age = row[5],
             country = row[6]
            ) for row in c.fetchall()]

            if user_role == 'admin':
                return render_template("home_admin.html", user_name=user_name, user_role=user_role, data=data)
            if user_role == 'regular':
                return render_template("home_regular.html", user_name=user_name, user_role=user_role, data=data)

        # e-mail filter
        elif "email_button" in request.form:
            e_mail = request.form.get('e_mail')
            c.execute('SELECT * FROM users WHERE email LIKE ?', ('%'+email+'%',))
            data = [dict(
             id = row[0],
             first_name = row[1],
             last_name = row[2],
             email = row[3],
             age = row[5],
             country = row[6]
            ) for row in c.fetchall()]

            if user_role == 'admin':
                return render_template("home_admin.html", user_name=user_name, user_role=user_role, data=data)
            if user_role == 'regular':
                return render_template("home_regular.html", user_name=user_name, user_role=user_role, data=data)



        # ------ Admin EDIT/DELETE functionality
        # response to edit button
        elif "edit_button" in request.form:
            row_id = request.form.get('row_value')
            return redirect(url_for('edit', id=row_id, user_name=user_name, user_role=user_role))


        # response to delete button
        elif "delete_button" in request.form:
            row_id = request.form.get('row_value')
            print(row_id)
            conn = sqlite3.connect('point72.db')
            c = conn.cursor()
            c.execute('DELETE FROM users WHERE rowid = ?;', (row_id,))
            conn.commit()
            return redirect(url_for('home', user_name=user_name, user_role=user_role))

        # ------- LOGOUT functionality ------
        elif "logout" in request.form:
            return redirect(url_for('login'))

    # if method is GET, for initial home page loading
    c.execute('SELECT * from users')
    data = [dict(
     id = row[0],
     first_name = row[1],
     last_name = row[2],
     email = row[3],
     age = row[5],
     country = row[6]
    ) for row in c.fetchall()]

    if user_role == 'admin':
        return render_template("home_admin.html", user_name=user_name, user_role=user_role, data=data)
    if user_role == 'regular':
        return render_template("home_regular.html", user_name=user_name, user_role=user_role, data=data)

@app.route('/edit/<id>/<user_name>/<user_role>', methods=['GET','POST'])
def edit(id, user_name, user_role):

    if request.method == "POST":
        conn = sqlite3.connect('point72.db')
        c = conn.cursor()
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        age = request.form.get('age')
        country = request.form.get('country')

        sql = ("UPDATE users SET first_name = ?, last_name = ?, email = ?, age = ?, country = ? WHERE id = ?")
        c.execute(sql,(first_name, last_name, email, age, country, id))
        conn.commit()
        return redirect(url_for('home', user_name=user_name, user_role=user_role))

    conn = sqlite3.connect('point72.db')
    c = conn.cursor()
    c.execute('SELECT * from users WHERE rowid = ?', (id,))
    action = c.fetchall()
    print(action)

    return render_template("edit.html", id=id)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
