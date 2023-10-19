from flask import Flask, render_template
from db_helpers import close_db, get_db
from settings import PAGE_SIZE

app = Flask(__name__)
app.teardown_appcontext(close_db)


@app.route("/", defaults={"page_number": 1})
@app.route("/page/<int:page_number>")
def render_page(page_number: int):
    try:
        db = get_db()
        estates = db.get_estates(
            take=PAGE_SIZE,
            skip=(page_number - 1) * PAGE_SIZE
        )
        count = db.get_estate_count()
        max_page = ((count - 1) // PAGE_SIZE) + 1

        page_range = 2
        lo = max(page_number - page_range, 1)
        hi = min(page_number + page_range, max_page)
        page_list: list[int | None] = list(range(lo, hi + 1))
        if hi != max_page:
            page_list += [None, max_page]
        if lo > 1:
            page_list.insert(0, None)
            page_list.insert(0, 1)

        return render_template(
            "index.jinja",
            estates=estates,
            total_estates=count,
            page_list=page_list,
            curr_page=page_number
        )
    except Exception:
        return render_template(
            "index.jinja",
            estates=[],
            total_estates=0,
            page_list=[],
            curr_page=page_number
        )
