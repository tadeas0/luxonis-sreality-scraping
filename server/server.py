from flask import Flask, render_template
from db import close_db, get_db

app = Flask(__name__)
app.teardown_appcontext(close_db)


@app.route("/")
def hello_world():
    try:
        db = get_db()
        res = db.execute("""
                    SELECT estate.id, estate.name, url FROM estate
                    LEFT JOIN image ON estate.id = image.estate_id
                    ORDER BY id
                """)
        if res:
            estate_dict = dict()
            for i in res.fetchall():
                id, name, url = i
                if id in estate_dict:
                    estate_dict[id]["image_urls"].append(url)
                else:
                    estate_dict[id] = {
                        "id": id,
                        "name": name,
                        "image_urls": [url]
                    }
            estates = list(estate_dict.values())
            return render_template("index.jinja", estates=estates)
        else:
            return render_template("index.jinja", estates=[])
    except Exception:
        return render_template("index.jinja", estates=[])
