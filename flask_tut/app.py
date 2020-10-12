from flask import Flask, redirect, url_for,render_template, flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '151649418616068fB46C3598083817101d3bCD33'


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


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
	return render_template("about.html", title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash("Account created for {}".format(form.username.data), 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == "admin@blog.com" and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful! Please check username and password', 'danger')
			print("IT DID NOT")
	return render_template('login.html', title='Login', form=form)




if __name__ == '__main__':
    app.run(debug=True)

