import os
import secrets
import requests
import json
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Blueprint
from cardealer import app, db, bcrypt
from cardealer.forms import RegistrationForm, LoginForm, UpdateAccountForm, CarForm
from cardealer.models import User, CarData
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('land_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.Name.data, company=form.Company.data, phone=form.Phone.data, CVR=form.CVR.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login_page'))
    return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('land_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(CVR=form.CVR.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('land_page'))
        else:
            flash('Login Unsuccessful. Please Check username and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/land_page")
@login_required
def land_page():
    return render_template("land_page.html")

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.CVR=form.CVR.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Account updated')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.CVR.data = current_user.CVR
        form.email.data = current_user.email
    
    if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("profile.html", title='profile', image_file=image_file, form=form)

@app.route("/list")
@login_required
def list():
    posts = CarData.query.all()
    return render_template("list.html", posts=CarData)

@app.route("/account")
def account():
    return render_template('account.html', title='account')


@app.route("/api")
@login_required
def apisite():
    return render_template('api.html')

#def api():
    #ApiUrl = "http://api.nrpla.de/"
    #url = ApiUrl + title() +"?api_token=iZ3T9knspElwMyglvXbFKaKXK8co5k0LKjLzke6Uirnaw5FuqtE20SXKI4ttrZIM&advanced=1"
    #req = requests.get('url')
    #data = json.loads(req.content)
    #return render_template('api.html', data=data)

@app.route("/selling", methods=['GET', 'POST'])
@login_required
def sell_vehicle():
    form = CarForm()
    if form.validate_on_submit():
        cardata = CarData(Brand=form.Brand.data, Model=form.Model.data, Engine=form.Engine.data, Colour=form.Colour.data, Comment=form.Comment.data)#, image_file2=form.image_file2.data)
        db.session.add(cardata)
        db.session.commit()
    
    return render_template('selling.html', form = form)

#@app.route("/selling", methods=['GET', 'POST'])
#@login_required
#def sell_vehicle():
    #form = CarForm()
    #if form.validate_on_submit():
        #POST = CarData(content=form.content.data)
        #db.session.add(CarData)
        #db.session.commit()
        #return redirect(url_for('land_page'))
    #return render_template('selling.html', form = form)

@app.route("/buying")
@login_required
def buy_vehicle():
    return render_template('buying.html')
    

@app.route("/contact")
def contact():
    return render_template('contact.html')
