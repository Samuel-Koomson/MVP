from flask import Flask, request, render_template, redirect, url_for, flash
from users.user import User

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Password does nor match", "danger")
        else:
            existing_users = User.find_by_field("username", username) +
            User.find_by_email("email", email)
            if existing_users:
                flash('Username or email already exists. Please choose a\
                different one.', 'danger')
            else:
                User.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                flash("Registration successful. You can now login.", "success")
                return redirect(url_for("login"))

    return render_template('register.html')
