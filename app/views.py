from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, make_response
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta
from .models import User, Cart, Product, Review, BuyHistory, Category
from .forms import RegisterForm, EditUserForm, AddProductForm, BuyProductForm
import os
from app import app, db
import logging

#set logging

logging.basicConfig(level=logging.NOTSET)
handler = logging.FileHandler('app.log', encoding='UTF-8')
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

@app.route('/')
@app.route('/index')
def index():
    app.logger.error('this is a error log')
    app.logger.warning('this is a warning log')
    app.logger.info('this is a info log')
    app.logger.debug('this is a debug log')
    # get the cookies
    email = request.cookies.get('email')
    password_candidate = request.cookies.get('password')
    # remember_me
    if email != None and password_candidate != None:
        user = User.query.filter_by(email=email).first()
        password = user.password
        if sha256_crypt.verify(password_candidate, password):
            session['logged_in'] = True
            session['name'] = user.name
            session['id'] = user.id
            if user.is_seller == True:
                session['is_seller'] = True
                flash('You are now logged in', 'success')
                return render_template('index.html')
            if user.is_admin == True:
                session['is_admin'] = True
                return render_template('index.html')
            cart = Cart.query.filter_by(user_id=user.id).all()
            cart_count = Cart.query.filter_by(user_id=user.id).count()

            # set cookies
            return render_template('index.html', cart=cart, cart_count=cart_count)

    return render_template('index.html')


@app.route('/collections')
def collections():
    result = session.get('logged_in')
    if result == None:
        product = Product.query.all()
        return render_template('collections.html', product=product)
    else:
        user = User.query.filter_by(name=session['name']).first()
        cart = Cart.query.filter_by(user_id=user.id).all()
        cart_count = Cart.query.filter_by(user_id=user.id).count()
        product = Product.query.all()
    return render_template('collections.html', product=product, cart=cart,cart_count=cart_count)

@app.route('/category/<string:category>')
def category(category):
    result = session.get('logged_in')
    if result == None:
        data = Category.query.filter_by(name=category).first()
        if data != None:
            product = data.products
            return render_template('category.html', category=category, product=product)
        else:
            return render_template('category.html', category=category)
    else:
        user = User.query.filter_by(name=session['name']).first()
        cart = Cart.query.filter_by(user_id=user.id).all()
        cart_count = Cart.query.filter_by(user_id=user.id).count()
        data = Category.query.filter_by(name=category).first()
        if data != None:
            product = data.products
            return render_template('category.html', category=category, product=product, cart=cart,cart_count=cart_count)
    return render_template('category.html', category=category)



@app.route('/about')
def about():
    result = session.get('logged_in')
    if result == None:
        return render_template('about.html')
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    return render_template('about.html',cart=cart,cart_count=cart_count)


@app.route('/terms')
def terms():
    result = session.get('logged_in')
    if result == None:
        return render_template('terms.html')
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    return render_template('terms.html',cart=cart,cart_count=cart_count)


@app.route('/contact')
def contact():
    result = session.get('logged_in')
    if result == None:
        return render_template('contact.html')
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    return render_template('contact.html', cart=cart, cart_count=cart_count)

@app.route('/collections/search', methods=['GET', 'POST'])
def search():
    result = session.get('logged_in')
    if result == None:
        if request.method == 'POST':
            text = request.form['search_txt']
            products = Product.query.filter(Product.name.contains(text)).all()
            result_count = Product.query.filter(Product.name.contains(text)).count()
            if result_count != 0:
                return render_template('search.html', text=text, products=products)
            else:
                flash('No Items found', 'warning')
                return render_template('search.html', text=text)
        return render_template('search.html')
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    if request.method == 'POST':
        text = request.form['search_txt']
        products = Product.query.filter(Product.name.contains(text)).all()
        result_count = Product.query.filter(Product.name.contains(text)).count()
        if result_count != 0:
            return render_template('search.html',text=text, products=products,cart=cart,cart_count=cart_count)
        else:
            flash('No Items found', 'warning')
            return render_template('search.html', text=text, cart=cart, cart_count=cart_count)
    return render_template('search.html',cart=cart,cart_count=cart_count)

# User register


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    form.dateofbirth.data = datetime.strptime("2018-01-01", "%Y-%m-%d")
    if request.method == 'POST' and form.validate():
        if form.is_seller.data == "Seller":
            is_seller = True
        else:
            is_seller = False
        sex = form.sex.data
        name = form.name.data
        address = form.address.data
        dateofbirth = form.dateofbirth.data
        country = form.country.data
        phone = form.phone.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        user = User.query.filter_by(email=email).first()
        if user != None:
            flash('This email has already been registered!', 'warning')
            return render_template('register.html', form=form)

        user = User(is_seller=is_seller, sex=sex, name=name, address=address,
                    dateofbirth=dateofbirth, country=country, phone=phone, email=email, password=password)
        db.session.add(user)
        # Commit to DB
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        remember_me = request.form.getlist('remember_me')

        user = User.query.filter_by(email=email).first()

        # set cookies expire time
        outdate = datetime.today() + timedelta(days=30)

        if user != None:
            # Get stored hash
            password = user.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed

                session['logged_in'] = True
                session['name'] = user.name
                session['id'] = user.id
                if user.is_seller == True:
                    session['is_seller'] = True
                    # set cookies
                    response=make_response(redirect(url_for('index')))
                    response.set_cookie('email',email, expires=outdate)
                    response.set_cookie('password',password_candidate, expires=outdate)
                    return response
                if user.is_admin == True:
                    session['is_admin'] = True
                    # set cookies
                    response=make_response(redirect(url_for('dashboard')))
                    response.set_cookie('email',email, expires=outdate)
                    response.set_cookie('password',password_candidate, expires=outdate)
                    return response
                session['count'] = Cart.query.filter_by(
                    user_id=user.id).count()
                products = Cart.query.filter_by(user_id=User.id).all()
                print(session['count'])
                if session['count'] != 0:
                    session['is_cart_notempty'] = True
                    session['product_name'] = products[0].product.name
                    session['product_img'] = products[0].product.image

                flash('You are now logged in', 'success')

                # set cookies
                response=make_response(redirect(url_for('index')))
                response.set_cookie('email',email, expires=outdate)
                response.set_cookie('password',password_candidate, expires=outdate)
                return response
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Email not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Check if user is a seller


def is_user_seller(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_seller' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Only seller', 'danger')
            return redirect(url_for('index'))
    return wrap

# Check if user is a admin


def is_user_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Only admin', 'danger')
            return redirect(url_for('index'))
    return wrap

# Logout


@app.route('/logout')
@is_logged_in
def logout():
    #clear session
    session.clear()
    flash('You are now logged out', 'success')
    #clear the cookies
    response=make_response(redirect(url_for('login')))
    response.delete_cookie('email')
    response.delete_cookie('password')
    return response


@app.route('/user_edit', methods=['GET', 'POST'])
@is_logged_in
def user_edit():
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    form = EditUserForm(request.form)
    form.sex.data = user.sex
    form.name.data = user.name
    form.address.data = user.address
    form.dateofbirth.data = user.dateofbirth
    form.country.data = user.country
    form.phone.data = user.phone
    form.email.data = user.email
    if request.method == 'POST' and form.validate():
        user.sex = request.form['sex']
        user.name = request.form['name']
        session['name'] = user.name
        user.address = request.form['address']
        user.dateofbirth = datetime.strptime(
            request.form['dateofbirth'], "%Y-%m-%d")
        user.country = request.form['country']
        user.phone = request.form['phone']
        user.email = request.form['email']
        user.password = sha256_crypt.encrypt(str(request.form['password']))

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user_edit.html', form=form, cart=cart,cart_count=cart_count)


@app.route('/checkout')
@is_logged_in
def checkout():
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    total_price = 0
    for item in cart:
        total_price += item.count*item.product.actual_price
    return render_template('checkout.html', cart=cart, cart_count=cart_count,total_price=total_price)


@app.route('/product/<string:product_id>')
def product(product_id):
    result = session.get('logged_in')
    if result == None:
        product = Product.query.filter_by(id=product_id).first()
        reviews = Review.query.filter_by(product_id=product.id).all()
        review_count = Review.query.filter_by(product_id=product.id).count()
        return render_template('product.html', product=product,reviews=reviews,product_id=product_id,review_count=review_count )
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    product = Product.query.filter_by(id=product_id).first()
    reviews = Review.query.filter_by(product_id=product.id).all()
    review_count = Review.query.filter_by(product_id=product.id).count()
    return render_template('product.html', product=product,reviews=reviews,product_id=product_id,review_count=review_count,cart=cart,cart_count=cart_count)

@app.route('/seller_product/<string:user_id>')
@is_logged_in
@is_user_seller
def seller_product(user_id):
    product = Product.query.filter_by(user_id=session['id']).all()
    return render_template('seller_product.html',product=product)

@app.route('/add_review/<string:product_id>', methods=['GET', 'POST'])
@is_logged_in
def post_review(product_id):
    if request.method == 'POST':
        text = request.form['review_text']
        user = User.query.filter_by(name=session['name']).first()
        user_id = user.id
        review = Review(user_id=user_id,product_id=product_id,text=text)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('product', product_id=product_id))
    return redirect(url_for('product', product_id=product_id))

@app.route('/add_cart/<string:product_id>', methods=['GET', 'POST'])
@is_logged_in
def add_cart(product_id):
    if request.method == 'POST':
        count = request.form['count']
        user = User.query.filter_by(name=session['name']).first()
        user_id = user.id
        cart = Cart(user_id=user_id,product_id=product_id,count=count)
        db.session.add(cart)
        db.session.commit()
        return redirect(url_for('checkout'))
    return render_template('checkout.html')

@app.route('/delete_cart/<string:product_id>', methods=['GET', 'POST'])
def delete_cart(product_id):
    cart = Cart.query.filter_by(product_id=product_id).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('checkout'))

@app.route('/edit_cart/<string:product_id>', methods=['GET', 'POST'])
def edit_cart(product_id):
    cart = Cart.query.filter_by(product_id=product_id).first()
    count = request.form['count']
    cart.count = count
    db.session.commit()
    return redirect(url_for('checkout'))

@app.route('/add_product', methods=('GET', 'POST'))
@is_logged_in
@is_user_seller
def add_product():
    form = AddProductForm(request.form)
    if request.method == 'POST' and form.validate():
        max_product = Product.query.order_by("-id").first()
        #set the only id for the product img
        if max_product == None:
            max_id = 1
        else:
            max_id = max_product.id+1
        category = request.form.getlist('category')
        name = form.name.data
        user_id = session['id']
        description = form.description.data
        origin_price = form.origin_price.data
        actual_price = form.actual_price.data
        #save the image to local path
        f = request.files['image']
        filename = secure_filename(f.filename)
        # get the file type of the upload image
        filetype = '.' + filename.split('.')[1]
        filename = str(max_id) + filetype
        basepath = os.path.dirname(__file__)  # current file path
        upload_path = os.path.join(
            basepath, 'static/images/photos/' + category[0], filename)
        f.save(upload_path)
        image = category[0] + '/' + filename
        product = Product(user_id=user_id, name=name, description=description, image=image, origin_price=origin_price, actual_price=actual_price)
        for item in category:
            categories = Category.query.filter_by(name=item).first()
            product.categories.append(categories)
        db.session.add(product)
        db.session.commit()
        flash('You have added a new product', 'success')
        return redirect(url_for('collections'))
    return render_template('add_product.html', form=form)

@app.route('/delete_product/<string:product_id>')
@is_logged_in
@is_user_seller
def delete_product(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    for item in reviews:
        db.session.delete(item)
    product = Product.query.filter_by(id=product_id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('seller_product', user_id=session['id']))


@app.route('/payment', methods=['GET', 'POST'])
@is_logged_in
def payment():
    user = User.query.filter_by(name=session['name']).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    cart_count = Cart.query.filter_by(user_id=user.id).count()
    form = BuyProductForm(request.form)
    if cart_count == 0:
        flash('Your cart is empty, please look around!', 'success')
        return redirect(url_for('collections'))
    if request.method == 'POST' and form.validate():
        user_id = user.id
        receiver_name = form.receiver_name.data
        address = form.address.data
        phone = form.phone.data
        payment_option = form.payment_option.data
        message = form.message.data
        for item in cart:
            product_id = item.product.id
            count = item.count
            buy_product = BuyHistory(user_id=user_id,product_id=product_id,count=count,receiver_name=receiver_name,address=address,phone=phone,payment_option=payment_option,message=message)
            db.session.add(buy_product)
            db.session.commit()
        old_cart = Cart.query.filter_by(user_id=user.id).all()
        for item in old_cart:
            db.session.delete(item)
            db.session.commit()
        return redirect(url_for('index'))

    return render_template('payment.html',cart=cart, cart_count=cart_count, form=form)

#Dashboard

@app.route('/dashboard')
@is_logged_in
@is_user_admin
def dashboard():
    return render_template('/dashboard/dashboard.html')


@app.errorhandler(404)
def page_not_found(e):
    app.logger.exception('error 404: %s', e)
    return render_template('error-404.html'), 404
