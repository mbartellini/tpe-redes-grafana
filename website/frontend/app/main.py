from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import escape
import requests 

app = Flask(__name__)
app.secret_key = "mi_clave_super_secreta"  

API_URL = "http://api:80"  

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("q", "").strip()
    medias = []

    if query:
        try:
            response = requests.get(f"{API_URL}/media/search/{query}")
            response.raise_for_status()
            medias = response.json()
        except requests.RequestException as e:
            print(f"Error fetching media from API: {e}")
            medias = []

    return render_template("home.html", medias=medias, query=query)

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
    try:
        response = requests.get(f"{API_URL}/media/{media_id}")
        response.raise_for_status()
        media = response.json()
        reviews_response = requests.get(f"{API_URL}/media/{media_id}/reviews")
        reviews = reviews_response.json() if reviews_response.status_code == 200 else []
        return render_template("media_details.html", media=media, reviews=reviews)
    except requests.RequestException as e:
        print(f"Error fetching media data: {e}")
        return "Error fetching media data", 500

@app.route('/media/<int:media_id>/reviews', methods=['POST'])
def add_review(media_id):
    try:
        content = request.form.get('content')

        review_data = {
            "content": content,
        }
        response = requests.post(f"{API_URL}/media/{media_id}/reviews",
            json=review_data,
            headers={"Authorization": f"Bearer {session.get('access_token')}"}
        )

        response.raise_for_status()
        return redirect(url_for('show_media', media_id=media_id))

    except requests.RequestException as e:
        print(f"Error submitting review: {e}")
        return redirect(url_for('show_media', media_id=media_id))

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