from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="user_system"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        session["username"] = username
        return redirect(url_for("dashboard"))
    else:
        return "Invalid Credentials!"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"Welcome {session['username']}!"
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
