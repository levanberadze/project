from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Levan_Beradze"
app.permanent_session_lifetime = timedelta(seconds=5)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # session.permanent = True
        user = request.form['user']
        session['user'] = user
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return render_template('profile.html', username=user)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
