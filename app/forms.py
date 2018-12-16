from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, validators, DateField, BooleanField, SelectField, FloatField, SelectMultipleField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import IMAGES, UploadSet


images = UploadSet('images', IMAGES)


class RegisterForm(Form):
    is_seller = SelectField("I'am", coerce=str, choices=[
                            ("Buyer", "Buyer"), ("Seller", "Seller")])
    sex = SelectField('Sex', coerce=str, choices=[("Mr", "Mr"), ("Ms", "Ms")])
    name = StringField('Name', [validators.Length(
        min=1, max=50), validators.DataRequired()])
    address = StringField('Address', [validators.Length(
        min=1, max=100), validators.DataRequired()])
    dateofbirth = DateField('Date of birth', format='%Y-%m-%d')
    country = SelectField('Country', coerce=str, choices=[
                          ("US", "United States"), ("Aus", "Australia"), ('Ch', 'China')])
    phone = StringField('Phone', [validators.DataRequired()])
    email = StringField(
        'Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Re-Enter Password', [validators.DataRequired()])


class EditUserForm(Form):
    sex = SelectField('Sex', coerce=str, choices=[("Mr", "Mr"), ("Ms", "Ms")])
    name = StringField('Name', [validators.Length(
        min=1, max=50), validators.DataRequired()])
    address = StringField('Address', [validators.Length(
        min=1, max=100), validators.DataRequired()])
    dateofbirth = DateField('Date of birth', format='%Y-%m-%d')
    country = SelectField('Country', coerce=str, choices=[
                          ("US", "United States"), ("Aus", "Australia"), ('Ch', 'China')])
    phone = StringField('Phone', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Re-Enter Password', [validators.DataRequired()])

# Add Product form


class AddProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=100)])
    description = StringField('Description', [validators.Length(min=0)])
    category = SelectMultipleField('Category', [validators.DataRequired()], coerce=str, choices=[("Men", "Men"), ("Women", "Women"), ('Gifts', 'Gifts')])
    origin_price = FloatField('Origin Price', [validators.DataRequired()])
    actual_price = FloatField('Actual Price', [validators.DataRequired()])

# Buy product form

class BuyProductForm(Form):
    sex = SelectField('Sex', coerce=str, choices=[("Mr", "Mr"), ("Ms", "Ms")])
    receiver_name = StringField('Receiver Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=100), validators.DataRequired()])
    payment_option = SelectField('Payment Option', coerce=str, choices=[("Cash", "Cash"), ("CreditCard", "CreditCard"), ("PayPal", "PayPal"), ("Alipay", "Alipay")])
    message = TextAreaField('Message')

# Item form


class ItemForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = StringField('Body', [validators.Length(min=0)])
    date = DateField('Date', format='%Y-%m-%d')
    complete = SelectField('Status', coerce=str, choices=[
                           ("True", "Complete"), ("False", "Incomplete")])
