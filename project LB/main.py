from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Levan_Beradze"
app.permanent_session_lifetime = timedelta(seconds=30)


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
    recipe = conn.execute('SELECT * FROM recipes WHERE recipe_id = ?', (recipe_id,)).fetchone()
    conn.close()
    return render_template('recipe.html', recipe=recipe)


@app.route('/add_recipe', methods=("GET", "POST"))
def add_recipe():
    if request.method == "POST":
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        try:
            conn = get_db_conn()
            conn.execute('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)', (title, ingredients, instructions))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error inserting data: {e}")
        finally:
            conn.close()
        return redirect('/')
    return render_template('add_recipe.html')


@app.route('/list')
def list():
    con = sqlite3.connect("recipes.db")
    con.row_factory = sqlite3.Row


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
