from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///records.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Records(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)



def __repr__(self) -> str:
        return f"{self.sno} - {self.categ}"


@app.route('/', methods = [ 'GET', 'POST'])
def expense_manager():
        if (request.method=='POST'):
            desc =request.form.get('desc')
            amnt =request.form.get('amnt')
            tags =request.form.get('tags')
            record=Records(descr=desc, amount=amnt, category= tags)
            db.session.add(record)
            db.session.commit()
        allrecord=Records.query.all()
        return render_template('index.html', allrecord=allrecord)


@app.route('/delete/<int:sno>')
def delete(sno):
    record = Records.query.filter_by(sno=sno).first()
    db.session.delete(record)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        desc = request.form['desc']
        amnt = request.form['amnt']
        tags = request.form['tags']
        record = Records.query.filter_by(sno=sno).first()
        record.descr = desc
        record.amount = amnt
        record.category = tags
        db.session.add(record)
        db.session.commit()
        return redirect("/")
    
    record = Records.query.filter_by(sno=sno).first()
    return render_template('update.html', record=record)

if __name__== "__main__":
    app.run(debug=True)

app.run()