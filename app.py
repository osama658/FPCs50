import os
import sqlite3
import helpers

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sheprokora.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# start empliminting the main page here!. TODO

@app.route("/")
@login_required
def main():
    """ the main page """
    # user_id = session["user_id"]
    return render_template("/main.html")



# sign up!
@app.route("/register", methods=["GET", "POST"]) # TODO -ABDALLH--notice that- The name of this route and the html file must be the same, (this route called "register")
def register():
    """Register user"""

    if (request.method == "POST"):
        # Get the username and the password
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Varified if the user failed to enter user name and password and confirm the password.
        if not username:
            return apology("Username is required!")
        elif not password:
            return apology("Password is required!")
        elif not confirmation:
            return apology("confirmation is required!")
        if password != confirmation:
            return apology("please type the same password twice!")

        # Generate hash code to this user!
        hash = generate_password_hash(password)

        # save the user data :)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",username, hash)
            return redirect('main.html')
        except sqlite3.IntegrityError:
            return apology("Username has already been registered!")

    # if the user failed to sign up ):
    else:
        return render_template("register.html")

# login!
@app.route("/login", methods=["GET", "POST"]) # TODO -ABDALLH--notice that- The name of this route and the html file must be the same, (this route called "login")
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

         # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM sheprokora WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("main.html")

     # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#logout!
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("main")




