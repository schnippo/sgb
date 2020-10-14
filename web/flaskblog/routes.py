from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt, PROPERTIES_PATH
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import os

posts = [
	{
	'author': 'Jonas Rose',
	'title': 'Blog Post 1',
	'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ullamcorper turpis leo, quis finibus risus rhoncus eget. Mauris lorem massa, convallis vitae suscipit in, feugiat maximus erat. ',
	'date_posted': 'April 20, 2018'
	},
	{
	'author': 'Simone Steiger',
	'title': 'Blog Post 2',
	'content': 'Donec eleifend a ligula ac pretium. Sed ac lectus et massa viverra tincidunt. In feugiat condimentum scelerisque. ',
	'date_posted': 'April 21, 2018'
	}]


def update_prop(prop, value):
	properties = {}
	lines = open(PROPERTIES_PATH, "r").readlines()
	for line in lines:
		properties[line.split()[0]] = line.split()[1]
	properties[prop] = value
	with open("properties", "w") as f:
		for key in properties:
			f.write(key + " " + properties[key] +"\n")
def get_prop_value(prop):
	properties = {}
	lines = open(PROPERTIES_PATH, "r").readlines()
	for line in lines:
		properties[line.split()[0]] = line.split()[1]
	return properties[prop]





@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about", methods=['GET'])
def about():
	return render_template("about.html", title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created! Your are now able to log in.", 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful! Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def dashboard():
	image_file = url_for('static', filename ='profile_pics/' + current_user.image_file )
	return render_template('controls.html', title='Controls', image_file = image_file)
	
# @login_required
@app.route("/controls", methods=["POST", "GET"])
def controls():
	placeholders = {
		"fan_value" : get_prop_value("pwm_dutycycle")
	}

	if request.method == 'POST':
		print(request.form)

		if request.form.get("relay_ID"):
			print("Detected Relay Input")
			ID = request.form.get('relay_ID')
			ONTIME = request.form.get('relay_ONTIME')
			OFFTIME = request.form.get('relay_OFFTIME')
			STARTDELAY = request.form.get('relay_STARTDELAY')
			values = f"{ID} {ONTIME} {OFFTIME} {STARTDELAY}\n"
			print(values)
			with open('output.txt', 'a') as f:
				f.write(values)
		elif request.form.get("fan_number"):
			print("Detected PWM Input")
			fan_number = request.form.get("fan_number")
			fan_value = request.form.get("fan_value")
			fan_mode = request.form.get("fan_mode")
			if fan_number == "9":
				print("fan 9")
				if fan_mode == 'manual':
					update_prop("pwm_mode", "manual")
					update_prop("pwm_dutycycle", fan_value)
					response = f"Updating properties to manual control with {fan_value}% dutycyle."
					print(response)
				else:
					update_prop("pwm_mode", "auto")
					response = f"Updating properties to automatic control."
					print(response)
				return render_template('controls.html', title='Controls', placeholders=placeholders, response=response)
			else:
				print(f"Change on Fan NR {fan_number}")
				response = os.system(f"python3 /home/jonas/git/ssgb/controllers/pwm/force_pwm_update.py {fan_number} {fan_value}")
				# sp_answer = subprocess.run(["/usr/bin/python3", "/home/jonas/git/controllers/pwm/force_pwm_update.py", str(fan_number), str(fan_value)])
				print(response)
				return render_template('controls.html', title='Controls', placeholders=placeholders, response=response)


	return render_template('controls.html', title='Controls', placeholders=placeholders)



