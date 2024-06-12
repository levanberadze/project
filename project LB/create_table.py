import sqlite3

conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL
)
''')

cursor.execute('''
INSERT INTO recipes (title, ingredients, instructions) VALUES
('Pancakes', 'Flour, Eggs, Milk, Sugar', 'Mix all ingredients and cook on a griddle.'),
('Scrambled Eggs', 'Eggs, Butter, Salt', 'Whisk eggs, melt butter in a pan, cook eggs and stir.')
''')
print("Created Table succesefully")

conn.commit()
conn.close()
