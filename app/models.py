from datetime import datetime
from app import db

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sex = db.Column(db.String(10), nullable=False)
	name = db.Column(db.String(200), nullable=False)
	address = db.Column(db.String(300), nullable=False)
	dateofbirth = db.Column(db.Date,nullable=False)
	country = db.Column(db.String(50), nullable=False)
	phone = db.Column(db.String(200),nullable=False)
	email = db.Column(db.String(200),nullable=False, unique=True)
	password = db.Column(db.String(300),nullable=False)
	create_date = db.Column(db.Date, default=datetime.utcnow)
	is_admin = db.Column(db.Boolean, default=False)
	is_seller = db.Column(db.Boolean, default=False)
	review = db.relationship('Review', backref='user', lazy='dynamic')
	cart = db.relationship('Cart', backref='user', lazy='dynamic')
	buyhistory = db.relationship('BuyHistory', backref='user', lazy='dynamic')
	product = db.relationship('Product', backref='user', lazy='dynamic')

registrations = db.Table('registrations',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    )

class Product(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	name = db.Column(db.String(30), nullable=False)
	description = db.Column(db.String(300))
	image = db.Column(db.String(100), nullable=False)
	origin_price = db.Column(db.Float, nullable=False)
	actual_price = db.Column(db.Float, nullable=False)
	published_at = db.Column(db.Date, default=datetime.utcnow)
	review = db.relationship('Review', backref='product', lazy='dynamic')
	cart = db.relationship('Cart', backref='product', lazy='dynamic')
	buyhistory = db.relationship('BuyHistory', backref='product', lazy='dynamic')
	categories = db.relationship('Category', secondary=registrations, backref=db.backref('products', lazy='dynamic'), lazy='dynamic')

class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String, nullable=False)

class Review(db.Model):
	__tablename__ = 'review'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
	text = db.Column(db.String(300), nullable=False)
	rating = db.Column(db.Integer, nullable=False, default=3)
	review_time = db.Column(db.Date, default=datetime.utcnow)

class Cart(db.Model):
	__tablename__ = 'cart'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
	count = db.Column(db.Integer)

class BuyHistory(db.Model):
	__tablename__ = 'buyhistory'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
	count = db.Column(db.Integer)
	receiver_name = db.Column(db.String, nullable=False)
	address = db.Column(db.String, nullable=False)
	phone = db.Column(db.String, nullable=False)
	payment_option = db.Column(db.String)
	buy_time = db.Column(db.Date, default=datetime.utcnow)
	message = db.Column(db.String)
	delivered = db.Column(db.Boolean, default=False)
	deliverTime = db.Column(db.Date, nullable=True)
