from app import app
from .forms import BookmarkForm, ContactForm, UserForm, UserLoginForm
from .models import db, Bookmark, Contact, User
from flask import render_template, request, redirect, flash
from flask_login import login_user, LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    users = User.query.order_by(User.username).all()
    return render_template('index.html', users=users)

@app.route('/add_user/', methods=['POST', 'GET'])
def add_user():
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                username = form.username.data
                email = form.email.data
                password = generate_password_hash(form.password.data, "sha256")
                image = form.image.data

                try:
                    if requests.get(image).status_code != 200:
                        image = "https://tmdstudios.files.wordpress.com/2022/01/blank_profile.png"
                except:
                    image = "https://tmdstudios.files.wordpress.com/2022/01/blank_profile.png"
                new_user = User(username, email, password, image)

                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/')
                except:
                    return 'Unable to create new user'
        flash("Passwords do not match")
        return render_template('add_user.html', form=form)

    return render_template('add_user.html', form=form)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Unable to delete user'

@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = UserLoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    return redirect('/')
                else:
                    flash("Wrong password")
            else:
                flash("User does not exist")

    return render_template('login.html', form=form)

@app.route('/logout/', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login/')

@app.route('/bookmarks/', methods=['POST', 'GET'])
@login_required
def bookmarks():
    form = BookmarkForm()
    # id = current_user.id
    
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            url = form.url.data
            description = form.description.data

            new_bookmark = Bookmark(name, url, description)

            try:
                db.session.add(new_bookmark)
                db.session.commit()
                return redirect('/bookmarks/')
            except:
                return 'Unable to add bookmark'    

    bookmarks = Bookmark.query.order_by(Bookmark.date_created).all()
    return render_template('bookmarks.html', bookmarks=bookmarks, form=form)

@app.route('/contacts/', methods=['POST', 'GET'])
@login_required
def contacts():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            number = form.number.data
            image = form.image.data

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

    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('contacts.html', contacts=contacts, form=form)

@app.route('/update_contact/<int:id>', methods=['POST', 'GET'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        if len(request.form.get("name")) <= 0:
            flash("Please enter a valid name")
            return render_template('update_contact.html', contact=contact)
        if len(request.form.get("email")) <= 0 or request.form.get("email").find('@') < 0:
            flash("Please enter a valid email")
            return render_template('update_contact.html', contact=contact)
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

    return render_template('update_contact.html', contact=contact)

@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    contact_to_delete = Contact.query.get_or_404(id)

    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/contacts/')
    except:
        return 'Unable to delete contact'

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_not_found(e):
    return render_template("500.html"), 500