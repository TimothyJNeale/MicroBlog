import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

import os

database = os.getenv('MICROBLOG_DATABASE')
username = os.getenv('MICROBLOG_USERNAME')
password = os.getenv('MICROBLOG_PASSWORD')

connection_string = f"mongodb+srv://{username}:{password}@{database}.rk10zip.mongodb.net/"

app = Flask(__name__)
client = MongoClient(connection_string)

entries = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entry_content = request.form['content']
        formated_date = datetime.datetime.today().strftime('%Y-%m-%d')
        entries.append((entry_content, formated_date))
        
    entries_with_date = [
        (
            entry[0], 
            entry[1], 
            datetime.datetime.strptime(entry[1], '%Y-%m-%d').strftime('%b %d')
        ) for entry in entries
    ]
    return render_template('home.html', entries=entries_with_date) 