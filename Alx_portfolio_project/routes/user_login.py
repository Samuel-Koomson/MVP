from flask import Flask, request, render_template, redirect, url_for, flash, session
from users.user import User

app = Flask(__name__)
app.secret_key = ""


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.find_by_field('username', username)
        if users:
            user = users[0]
            if user.password == password:
                session['user_id'] = user.id
                flash('Login successful.', 'success')
                return redirect(url_for('dashboard'))
        flash("Invalid username or password.", "danger")
    return render_template('login.html')


if __name__=='__main__':
    app.run(debug=True)
