import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

import os

database = os.getenv('MICROBLOG_DATABASE')
username = os.getenv('MICROBLOG_USERNAME')
password = os.getenv('MICROBLOG_PASSWORD')

connection_string = f"mongodb+srv://{username}:{password}@{database}.qvo1l4s.mongodb.net/"

app = Flask(__name__)
client = MongoClient(connection_string)
app.db = client.microblog


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entry_content = request.form['content']
        formated_date = datetime.datetime.today().strftime('%Y-%m-%d')
        app.db.entries.insert_one({'content': entry_content, 'date': formated_date})
        

    # Create list comprehension from entries to add formatted date
    entries_with_date = [
    (
        entry['content'], 
        entry['date'], 
        datetime.datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d')
    ) for entry in app.db.entries.find({})
    ]

    return render_template('home.html', entries=entries_with_date) 