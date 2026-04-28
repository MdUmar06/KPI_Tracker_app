from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE Employee_Email=? AND Password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["email"] = user["Employee_Email"]
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT Employee_Code, Employee_Name, Employee_Email, 
           Club_Name, KPI_1, KPI_2, KPI_3, Avg_KPI 
           FROM users WHERE Employee_Email=?""",
        (session["email"],)
    )

    user = cursor.fetchone()
    conn.close()

    return render_template("dashboard.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)