from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import escape
import requests 

app = Flask(__name__)
app.secret_key = "mi_clave_super_secreta"  

API_URL = "http://api:80"  

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/user/<userId>',methods=['GET'])
def show_user_profile(userId):
    try:
        userId = int(userId)
        response = requests.get(f"{API_URL}/users/{userId}")
        response.raise_for_status()
        user= response.json()
    except requests.RequestException as e:
        print(f"Error retrieving user: {e}")
        return "Error retrieving user", 500
    return render_template("user_profile.html", user=user)

@app.route('/media/<int:media_id>')
def show_media(media_id):
    return f'Media {media_id}'


@app.route("/login", methods=["GET", "POST"])
def login():
    if "access_token" in session and "user_id" in session:
        # Si ya está logueado, redirigir al perfil
        return redirect(url_for("show_user_profile", userId=session["user_id"]))

    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Enviar la api
        response = requests.post(f"{API_URL}/login/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            print("Login exitoso")
            data = response.json()
            session["access_token"] = data["access_token"]
            session["user_id"] = data["user_id"]
            return redirect(url_for("show_user_profile", userId=data["user_id"]))
        else:
            error = "User or password incorrect"

    return render_template("login.html", error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            error = "Passwords don't match"
        else:
            # Enviar la petición a la API para crear usuario
            response = requests.post(f"{API_URL}/users/", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 201:  
                return redirect(url_for('login'))
            else:
                try:
                    error = response.json().get('detail', 'Error registering user')
                except Exception:
                    error = "Error registering user"

    return render_template('register.html', error=error)

@app.route("/logout")
def logout():
    session.clear()  
    return redirect(url_for("home"))  