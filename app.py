import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/fanbook', methods=['POST'])
def fan_post():
    nickname = request.form['nick_give']
    msg = request.form['msg_give']

    doc = {
        'nickname': nickname,
        'msg': msg
    }
    db.fanbook.insert_one(doc)
    return jsonify({
        'msg': 'Data Berhasil Masuk'
    })

@app.route('/fanbook', methods=["GET"])
def fan_get():
    fan_list = list(db.fanbook.find({},{'_id': False}))
    return jsonify({
        'fan': fan_list
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
