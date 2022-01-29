from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Optional, EqualTo, Length
from wtforms.widgets import TextArea

class BookmarkForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    description = StringField("Description", validators=[Optional()], widget=TextArea())
    submit = SubmitField("Add Bookmark")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    number = StringField("Number", validators=[Optional()])
    image = StringField("Image", validators=[Optional()])
    submit = SubmitField("Add Contact")

class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm_password", "Passwords must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    image = StringField("Image", validators=[Optional()])
    submit = SubmitField("Sign Up")

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm_password", "Passwords must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Log In")