from flask import Flask, render_template
from db_helpers import close_db, get_db

app = Flask(__name__)
app.teardown_appcontext(close_db)


@app.route("/")
def render_estates():
    try:
        db = get_db()
        estates = db.get_estates()
        print(estates[0])
        return render_template("index.jinja", estates=estates)
    except Exception:
        return render_template("index.jinja", estates=[])
