from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
import secrets


# Configure application
app = Flask(__name__)

# Configure secret key for session management
app.secret_key = secrets.token_hex(32)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///lulus.db")

# Define a login_required decorator


@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect(url_for('login'))
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        # Get the values of the three input fields from the request
        input_nis = request.form.get("nis")
        input_tempat = request.form.get("tl")
        input_tanggal = request.form.get("tanggal")
        input_bulan = request.form.get("bulan")
        input_tahun = request.form.get("tahun")

        # Check if any of the input fields is empty
        if not input_nis or not input_tempat or not input_tanggal or not input_bulan or not input_tahun:
            flash("Lengkapi semua form terlebih dahulu", "warning")
            return render_template("login.html")

        rows = db.execute(
            "SELECT * FROM user WHERE nis = ? AND tl = ? AND tgl = ? AND bln = ? AND thn =?", input_nis, input_tempat, input_tanggal, input_bulan, input_tahun)
        # Check if a user was found with the given credentials
        if len(rows) != 1:
            flash("Data tidak sesuai!!", "danger")
            return render_template("login.html")

        # Log the user in by storing their id in the session
        session["user_id"] = rows[0]["nis"]
        # Redirect the user to the homepage
        nama = db.execute("SELECT nama FROM user WHERE nis=?", input_nis)
        nisn2 = db.execute("SELECT nisn FROM identitas WHERE nis=?", input_nis)
        kelas2 = db.execute("SELECT kelas FROM identitas WHERE nis=?", input_nis)
        ortu2 = db.execute("SELECT ortu FROM identitas WHERE nis=?", input_nis)
        pk2 = db.execute("SELECT pk FROM identitas WHERE nis=?", input_nis)
        kk2 = db.execute("SELECT kk FROM identitas WHERE nis=?", input_nis)

        nm = nama[0]["nama"]
        nisn = nisn2[0]["nisn"]
        ortu = ortu2[0]["ortu"]
        kelas = kelas2[0]["kelas"]
        pk = pk2[0]["pk"]
        kk = kk2[0]["kk"]

        return render_template("index.html", nm=nm, nisn=nisn, kelas=kelas, ortu=ortu, pk=pk, kk=kk, input_tempat=input_tempat, input_tanggal=input_tanggal, input_bulan=input_bulan, input_tahun=input_tahun, input_nis=input_nis)
    else:
        # Render the login page
        return render_template("login.html")
