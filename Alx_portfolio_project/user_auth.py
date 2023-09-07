from flask import Flask, request, render_template, redirect, url_for, flash, session
from users.user import User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "a secret key to be inserted"

bcrypt = Bcrypt(app)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.find_by_field('username', username)

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash("Login successful.", "success")
            return redirect(url_for('dashboard'))

        flash("Invalid username or password." "danger")

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

if __name__=="___main__":
    app.run(debug=True)
