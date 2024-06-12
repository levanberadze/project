from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(seconds=30)


class User:
    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username

    def register(self):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password, username) VALUES (?, ?)', (self.email, self.password, self.username))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (self.username,))
        record = cursor.fetchone()
        conn.close()
        if record == self.password:
            return True
        else:
            return False


def get_db_conn():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    conn = get_db_conn()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template("home.html", recipes=recipes)



@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    conn = get_db_conn()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    conn.close()
    return render_template('recipe.html', recipe=recipe)


@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        try:
            conn = get_db_conn()
            conn.execute('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)', (title, ingredients, instructions))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        except:
            flash("ar daemata recepti")
            return redirect(url_for('home'))
    return render_template("add_recipe.html")


@app.route('/edit_recipe/<int:recipe_id>', methods=["GET", "POST"])
def edit_recipe(recipe_id):
    conn = get_db_conn()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    if request.method == "POST":
        title = request.form["title"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        try:
            conn.execute('UPDATE recipes SET title = ?, ingredients = ?, instructions = ? WHERE id = ?',(title, ingredients, instructions, recipe_id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        except:
            flash('ver sheicvala recepti')
            return redirect(url_for('home'))
    conn.close()
    return render_template("edit_recipe.html", recipe=recipe)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
