from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ContactDB.db'
app.config['SQLALCHEMY_BINDS'] = {'userdb' : 'sqlite:///userdb.db'}
db = SQLAlchemy(app)

class userdb(db.Model):
    __bind_key__ = 'userdb'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail_id = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "User : " + str(self.id)

class ContactDB(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    number =  db.Column(db.Text, nullable=False, default='N/A')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Contact : " + str(self.id)

@app.route('/')
def main():
    return render_template('signin.html')

@app.route('/signin/new_user',methods=['GET','POST'])
def new_user():
    if request.method=='POST':
        print("initiated signin")
        mail_id = request.form['mail_id']
        password = request.form['password']
        new_user = userdb(mail_id = mail_id, password=password)
        db.session.add(new_user)
        db.session.commit()
        print('user added'+mail_id+password)
        return redirect('/contacts')
    else:
        return render_template('contacts.html')

@app.route('/signin/existing_user',methods=['GET','POST'])
def exisiting_user():
    if request.method=='POST':
        mail_id = request.form['mail_id']
        password = request.form['password']
        return render_template('contacts.html')
    else:
        return render_template('signin.html')

@app.route('/contacts',methods=['GET','POST',"DELETE"])
def contacts():
    if request.method=='POST':
        name_data = request.form['name']
        mail_data = request.form['mail']
        number_data = request.form['number']
        new_contact = ContactDB(name=name_data,mail=mail_data,number=number_data)
        db.session.add(new_contact)
        db.session.commit()
        print(new_contact)
        return redirect('/contacts')
    else:
        all_contacts = ContactDB.query.order_by(ContactDB.date_created).all()
        return render_template('contacts.html',contacts=all_contacts)

@app.route('/contacts/delete/<int:id>')
def delete(id):
    delete_contact = ContactDB.query.get(id)
    db.session.delete(delete_contact)
    db.session.commit()
    return redirect('/contacts')

@app.route('/contacts/search',methods=['GET','POST'])
def search():
    if request.method=="POST":
        number_data=request.form['search']
        search_contact = ContactDB.query.filter_by(number=number_data)
        # db.session.add(search_post)
        # db.session.commit()
        return render_template('search.html',contacts=search_contact)
    else:
        all_contacts = ContactDB.query.all()
        return render_template('contacts.html',contacts=all_contacts)

@app.route('/contacts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    if  request.method=='POST':
        contact = ContactDB.query.get(id)
        contact.name = request.form['name']
        contact.number = request.form['number']
        db.session.commit()
        return redirect('/contacts')
    else:
        this_contact=ContactDB.query.get(id)
        return render_template('edit.html',contacts=this_contact,id=id)

@app.route('/next/<string:name>', methods=['GET','POST'])
def next(name):
    return "Helllo next bro : " + name

if __name__=="__main__":
    app.run(debug=True)
