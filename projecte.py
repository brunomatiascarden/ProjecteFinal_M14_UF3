from flask import Flask, render_template, request, session, redirect, url_for
import requests
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bc998811'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)


@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pokemon WHERE usuario=%s", (username,))
    user = cur.fetchone()
    cur.close()

    if user is None:
        return "El usuario no existe"
    else:
        if password == user[2]:
            session['usuario'] = user[1]
            return redirect(url_for('index'))
        else:
            return "Contraseña incorrecta"


@app.route("/")
def login_form():
    return render_template('login.html')


@app.route("/index")
def index():
    return render_template('index.html')


# Harry Potter
@app.route('/search', methods=['POST'])
def search():
    character_id = request.form['character_id']
    
    # Realizar la solicitud a la API de Harry Potter para obtener la información del personaje
    response = requests.get(f'https://harry-potter-api.onrender.com/personajes/{character_id}')
    
    if response.status_code == 200:
        personaje = response.json()
    else:
        personaje = None
    
    return render_template('index.html', personaje=personaje)


if __name__ == '__main__':
    app.run(debug=True)
