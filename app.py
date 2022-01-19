from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(200))
    image = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, number, image):
        self.name = name
        self.email = email
        self.number = number
        self.image = image

    def __repr__(self):
        return f'<Contact {self.id}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts/', methods=['POST', 'GET'])
def contacts():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        image = request.form.get("image")
        try:
            if requests.get(image).status_code != 200:
                image = "https://tmdstudios.files.wordpress.com/2022/01/blank_profile.png"
        except:
            image = "https://tmdstudios.files.wordpress.com/2022/01/blank_profile.png"
        new_contact = Contact(name, email, number, image)

        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect('/contacts/')
        except:
            return 'Unable to add contact'
    else:
        contacts = Contact.query.order_by(Contact.name).all()
        return render_template('contacts.html', contacts=contacts)

@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    contact_to_delete = Contact.query.get_or_404(id)

    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/contacts/')
    except:
        return 'Unable to delete contact'

@app.route('/update_contact/<int:id>', methods=['POST', 'GET'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form.get("name")
        contact.email = request.form.get("email")
        contact.number = request.form.get("number")
        image = request.form.get("image")
        try:
            if requests.get(image).status_code != 200:
                image = "https://tmdstudios.files.wordpress.com/2022/01/blank_profile.png"
        except:
            image = "https://tmdstudios.files.wordpress.com/2022/01/blank_profile.png"
        contact.image = image

        try:
            db.session.commit()
            return redirect('/contacts/')
        except:
            return 'Unable to update contact'
    else:
        return render_template('update_contact.html', contact=contact)

if __name__ == "__main__":
    app.run(debug=True)