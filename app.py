import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(DateTime)
    aid = db.Column(db.Integer)
    qid = db.Column(db.Integer)
    state = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    reason = db.Column(db.String(100))
    task = db.Column(db.Float)

    def __init__(self, created_date, aid, qid, state, amount, reason, task):
        self.created_date = created_date
        self.aid = aid
        self.qid = qid
        self.state = state
        self.amount = amount
        self.reason = reason
        self.task = task



@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", records=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':

        aid = request.form['aid']
        qid = request.form['qid']
        state = request.form['state']
        amount = request.form['amount']
        reason = request.form['reason']
        task = request.form['task']

        my_data = Data(datetime,aid, qid, state, amount, reason, task)
        db.session.add(my_data)
        db.session.commit()

        flash("Record Inserted Successfully")

        return redirect(url_for('Index'))



@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.aid = request.form['aid']
        my_data.qid = request.form['qid']
        my_data.state = request.form['state']
        my_data.state = request.form['state']
        my_data.amount = request.form['amount']
        my_data.reason = request.form['reason']
        my_data.task = request.form['task']

        db.session.commit()
        flash("Record Updated Successfully")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Record Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
