import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Set up the app (flask documentation and finance pset)
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///tournament.db")

# Homepage. Nothing dynamic about this page. Just a welcome and some pictures.
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Displays all of the info the user input when they registered
@app.route("/profile")
def profile():
    username = session["user_id"]
    first_name = db.execute("SELECT first_name FROM athlete_info WHERE username = ?", username)[0]["first_name"]

    # Makes sure the user has already registered. If so, displays profile info.
    if first_name == None:
        return render_template("profile.html")
    else:
        last_name = db.execute("SELECT last_name FROM athlete_info WHERE username = ?", username)[0]["last_name"]
        name = first_name + " " + last_name
        age = db.execute("SELECT age FROM athlete_info WHERE username = ?", username)[0]["age"]
        rank = db.execute("SELECT rank FROM athlete_info WHERE username = ?", username)[0]["rank"]
        weight = str(db.execute("SELECT weight FROM athlete_info WHERE username = ?", username)[0]["weight"]) + " " + "lbs"
        return render_template("profile.html", name=name, age=age, rank=rank, weight=weight)

# It's possible this function does nothing, but I'm a bit afraid to delete it.
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # Make sure user is behaving
        if not username or not password or not confirm:
            return render_template("apology.html")
        else:
            user_id = session["user_id"]
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users(user_id, password) VALUES(?, ?)", user_id, password_hash)
            return render_template("register.html")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
# This is essentially the code from the CS50x Finance pset.

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            apology = "Please enter username and password."
            return render_template("apology.html", apology=apology)

        # Ensure password was submitted
        elif not request.form.get("password"):
            apology = "Please enter username and password."
            return render_template("apology.html", apology=apology)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            apology = "Either username does not exist or password does not match."
            return render_template("apology.html", apology=apology)

        # Remember which user has logged in
        session["user_id"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/tournaments", methods=["GET", "POST"])
def tournaments():
    if request.method == "POST":
        return render_template("fake_io.html")

    else:
        return render_template("tournaments.html")


@app.route("/create_profile", methods=["GET", "POST"])
def create_profile():
    if request.method == "POST":
        # Create variables to use
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = generate_password_hash(password)
        confirm = request.form.get("confirm")
        session["user_id"] = username

        # Checking if the username already exsists
        existing_users = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(existing_users) == 1:
            apology = "Username already exists"
            session.clear()
            return render_template("apology.html", apology=apology)
        # Checking if the user typed in a username and matching passwords
        elif not username:
            session.clear()
            apology = "Enter a username"
            return render_template("apology.html", apology=apology)
        elif not password or password != confirm:
            session.clear()
            apology = "Password and Confirmation must match"
            return render_template("apology.html", apology=apology)
        else:
            # If everything looks good, insert the info into the tables and render the athlete info page
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password_hash)
            db.execute("INSERT INTO athlete_info (username) VALUES (?)", username)
        return render_template("athlete_info.html")
    else:
        return render_template("create_profile.html")

@app.route("/athlete_info", methods=["GET", "POST"])
def athlete_info():
    if request.method == "POST":
        # Getting variables
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        rank = request.form.get("rank")
        weight = request.form.get("weight")
        username = session["user_id"]

        if not first_name or not last_name or not age or not rank or not weight:
            return render_template("apology.html")
        else:
            # If all looks good, insert info into the athlete info table
            db.execute("UPDATE athlete_info SET first_name = ?, last_name = ?, age = ?, rank = ?, weight = ? WHERE username = ?", first_name, last_name, age, rank, weight, username)
            name = first_name + " " + last_name
            weight = str(weight) + " " + "lbs"
            return render_template("profile.html", name=name, age=age, rank=rank, weight=weight)
    else:
        return render_template("athlete_info.html")

@app.route("/fake_io", methods=["GET", "POST"])
def fake_io():
    if request.method == "POST":
        username = session["user_id"]
        first_name = db.execute("SELECT first_name FROM athlete_info WHERE username = ?", username)[0]["first_name"]
        last_name = db.execute("SELECT last_name FROM athlete_info WHERE username = ?", username)[0]["last_name"]
        name = first_name + " " + last_name
        age = db.execute("SELECT age FROM athlete_info WHERE username = ?", username)[0]["age"]
        weight = db.execute("SELECT weight FROM athlete_info WHERE username = ?", username)[0]["weight"]
        rank = db.execute("SELECT rank FROM athlete_info WHERE username = ?", username)[0]["rank"]

        if age < 18:
            return render_template("apology.html")

        elif age >= 18 and age < 30:
            check = len(db.execute("SELECT * FROM adult WHERE name = ?", name))
            if check != 0:
                apology = "You are already registered for this tournament."
                return render_template("apology.html", apology=apology)
            else:
                db.execute("INSERT INTO adult (name, rank, weight) VALUES (?, ?, ?)", name, rank, weight)
                return render_template("success.html")

        elif age >= 30 and age < 40:
            check = len(db.execute("SELECT * FROM master WHERE name = ?", name))
            if check != 0:
                apology = "You are already registered for this tournament"
                return render_template("apology.html", apology=apology)
            else:
                db.execute("INSERT INTO master (name, rank, weight) VALUES (?, ?, ?)", name, rank, weight)
                return render_template("success.html")

        elif age >=40 and age < 50:
            check = len(db.execute("SELECT * FROM grandmaster WHERE name = ?", name))
            if check != 0:
                apology = "You are already registered for this tournament"
                return render_template("apology.html", apology=apology)
            else:
                db.execute("INSERT INTO grandmaster (name, rank, weight) VALUES (?, ?, ?)", name, rank, weight)
                return render_template("success.html")

        else:
            check = len(db.execute("SELECT * FROM graveyard WHERE name = ?", name))
            if check != 0:
                apology = "You are already registered for this tournament"
                return render_template("apology.html", apology=apology)
            else:
                db.execute("INSERT INTO graveyard (name, rank, weight) VALUES (?, ?, ?)", name, rank, weight)
                return render_template("success.html")

    return render_template("fake_io.html")

@app.route("/fakeio_bracket", methods=["GET"])
def fakeio_bracket():
    # Adult divisions
    # White Belts
    ad_wb_light = db.execute("SELECT name FROM adult WHERE rank = ? and weight <= ?", "White Belt", 175)
    ad_wb_heavy = db.execute("SELECT name FROM adult WHERE rank = ? and weight > ?", "White Belt", 175)
    # Blue Belts
    ad_blub_light = db.execute("SELECT name FROM adult WHERE rank = ? and weight <= ?", "Blue Belt", 175)
    ad_blub_heavy = db.execute("SELECT name FROM adult WHERE rank = ? and weight > ?", "Blue Belt", 175)
    # Purple Belts
    ad_pb_light = db.execute("SELECT name FROM adult WHERE rank = ? and weight <= ?", "Purple Belt", 175)
    ad_pb_heavy = db.execute("SELECT name FROM adult WHERE rank = ? and weight > ?", "Purple Belt", 175)

    # Brown Belts
    ad_brb_light = db.execute("SELECT name FROM adult WHERE rank = ? and weight <= ?", "Brown Belt", 175)
    ad_brb_heavy = db.execute("SELECT name FROM adult WHERE rank = ? and weight > ?", "Brown Belt", 175)

    # Black Belts
    ad_blab_light = db.execute("SELECT name FROM adult WHERE rank = ? and weight <= ?", "Black Belt", 175)
    ad_blab_heavy = db.execute("SELECT name FROM adult WHERE rank = ? and weight > ?", "Black Belt", 175)

    # Master divisions
    # White Belts
    ms_wb_light = db.execute("SELECT name FROM master WHERE rank = ? and weight <= ?", "White Belt", 175)
    ms_wb_heavy = db.execute("SELECT name FROM master WHERE rank = ? and weight > ?", "White Belt", 175)

    # Blue Belts
    ms_blub_light = db.execute("SELECT name FROM master WHERE rank = ? and weight <= ?", "Blue Belt", 175)
    ms_blub_heavy = db.execute("SELECT name FROM master WHERE rank = ? and weight > ?", "Blue Belt", 175)

    # Purple Belts
    ms_pb_light = db.execute("SELECT name FROM master WHERE rank = ? and weight <= ?", "Purple Belt", 175)
    ms_pb_heavy = db.execute("SELECT name FROM master WHERE rank = ? and weight > ?", "Purple Belt", 175)

    # Brown Belts
    ms_brb_light = db.execute("SELECT name FROM master WHERE rank = ? and weight <= ?", "Brown Belt", 175)
    ms_brb_heavy = db.execute("SELECT name FROM master WHERE rank = ? and weight > ?", "Brown Belt", 175)

    # Black Belts
    ms_blab_light = db.execute("SELECT name FROM master WHERE rank = ? and weight <= ?", "Black Belt", 175)
    ms_blab_heavy = db.execute("SELECT name FROM master WHERE rank = ? and weight > ?", "Black Belt", 175)

    # Grandmaster divisions
    # White Belts
    gm_wb_light = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight <= ?", "White Belt", 175)
    gm_wb_heavy = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight > ?", "White Belt", 175)

    # Blue Belts
    gm_blub_light = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight <= ?", "Blue Belt", 175)
    gm_blub_heavy = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight > ?", "Blue Belt", 175)

    # Purple Belts
    gm_pb_light = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight <= ?", "Purple Belt", 175)
    gm_pb_heavy = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight > ?", "Purple Belt", 175)

    # Brown Belts
    gm_brb_light = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight <= ?", "Brown Belt", 175)
    gm_brb_heavy = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight > ?", "Brown Belt", 175)

    # Black Belts
    gm_blab_light = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight <= ?", "Black Belt", 175)
    gm_blab_heavy = db.execute("SELECT name FROM grandmaster WHERE rank = ? and weight > ?", "Black Belt", 175)

    # Graveyard divisions
    # White Belts
    gv_wb_light = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight <= ?", "White Belt", 175)
    gv_wb_heavy = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight > ?", "White Belt", 175)

    # Blue Belts
    gv_blub_light = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight <= ?", "Blue Belt", 175)
    gv_blub_heavy = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight > ?", "Blue Belt", 175)

    # Purple Belts
    gv_pb_light = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight <= ?", "Purple Belt", 175)
    gv_pb_heavy = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight > ?", "Purple Belt", 175)

    # Brown Belts
    gv_brb_light = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight <= ?", "Brown Belt", 175)
    gv_brb_heavy = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight > ?", "Brown Belt", 175)

    # Black Belts
    gv_blab_light = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight <= ?", "Black Belt", 175)
    gv_blab_heavy = db.execute("SELECT name FROM graveyard WHERE rank = ? and weight > ?", "Black Belt", 175)

    return render_template("fakeio_bracket.html", ad_wb_light=ad_wb_light, ad_wb_heavy=ad_wb_heavy,
                            ad_blub_light=ad_blub_light, ad_blub_heavy=ad_blub_heavy, ad_pb_light=ad_pb_light,
                            ad_pb_heavy=ad_pb_heavy, ad_brb_light=ad_brb_light, ad_brb_heavy=ad_brb_heavy,
                            ad_blab_light=ad_blab_light, ad_blab_heavy=ad_blab_heavy, ms_wb_light=ms_wb_light,
                            ms_wb_heavy=ms_wb_heavy, ms_blub_light=ms_blub_light, ms_blub_heavy=ms_blub_heavy,
                            ms_pb_light=ms_pb_light, ms_pb_heavy=ms_pb_heavy, ms_brb_light=ms_brb_light,
                            ms_brb_heavy=ms_brb_heavy, ms_blab_light=ms_blab_light, ms_blab_heavy=ms_blab_heavy,
                            gm_wb_light=gm_wb_light, gm_wb_heavy=gm_wb_heavy, gm_blub_light=gm_blub_light,
                            gm_blub_heavy=gm_blub_heavy, gm_pb_light=gm_pb_light, gm_pb_heavy=gm_pb_heavy,
                            gm_brb_light=gm_brb_light, gm_brb_heavy=gm_brb_heavy, gm_blab_light=gm_blab_light,
                            gm_blab_heavy=gm_blab_heavy, gv_wb_light=gv_wb_light, gv_wb_heavy=gv_wb_heavy,
                            gv_blub_light=gv_blub_light, gv_blub_heavy=gv_blub_heavy, gv_pb_light=gv_pb_light,
                            gv_pb_heavy=gv_pb_heavy, gv_brb_light=gv_brb_light, gv_brb_heavy=gv_brb_heavy,
                            gv_blab_light=gv_blab_light, gv_blab_heavy=gv_blab_heavy)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
