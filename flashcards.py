from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for)

from model import db, save_db
import pandas as pd

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template(
        "welcome.html",
        cards=db
    )


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template(
            "card.html",
            card=card,
            index=index,
            max_index=len(db) - 1
        )
    except IndexError:
        abort(404)


@app.route("/add_card/", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {"question": request.form['question'],
                "answer": request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db) - 1))
    else:
        return render_template("add_card.html")


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            db.remove(db[index])
            save_db()
            return redirect(url_for('welcome'))
        else:
            card = db[index]
            return render_template("remove_card.html", card=card, index=index)
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list():
    return jsonify(db)


@app.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f)
        return data_xls.to_html()
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''
