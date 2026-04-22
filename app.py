from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# Secret key for sessions (required for login)
app.secret_key = "1234567890"

# -----------------------------
# Initialize database
# -----------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Home page (send + view wishes)
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO wishes (name, message) VALUES (?, ?)",
            (name, message)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("index.html")

# -----------------------------
# Login page
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == "1234":
            session["admin"] = True
            return redirect("/admin")
        else:
            return "❌ Wrong password"

    return render_template("login.html")

# -----------------------------
# Admin dashboard (protected)
# -----------------------------
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    #all wishes
    cursor.execute("SELECT * FROM wishes")
    wishes = cursor.fetchall()
    #total count
    cursor.execute("SELECT COUNT(*) FROM wishes")
    total_wishes=cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html", 
        wishes=wishes,
        total_wishes=total_wishes
        )

#----------------------------
#admin delete
#-------------------------
@app.route("/delete/<int:id>")
def delete_wish(id):
    if not session.get("admin"):
        return redirect("/login")
    
    conn = sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM wishes WHERE id =?",(id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")
#----------------------------
#Run app
#---------------------------
if __name__=="__main__":
    print("Birthday wishes App Running")
    app.run(debug=True)