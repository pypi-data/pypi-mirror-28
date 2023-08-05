from flask import Flask, jsonify, render_template

from newsbeuter_spread.db import DB


app = Flask(__name__)
db = DB()


@app.route('/')
def index():
    items = list(db.get_unread())
    return render_template('index.html', items=items)


@app.route('/read/<id>/', methods=['POST', ])
def read(id):
    db.mark_read(id)
    return jsonify({'status': 'success'})
