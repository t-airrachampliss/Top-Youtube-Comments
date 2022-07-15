from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'fba6ae164c4947ac5b3c9f2be7d6a488'

# App Home Page; Search bar and results
@app.route("/")
def search():
    return render_template('search.html', subtitle='Search Page', text='This is the search page')
   
# Page to register for an account
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home.html'))
    return render_template('register.html', title='Register', form=form)

# Page to login to existing account
# @app.route("/login")
#     return render_template('login.html', subtitle='Results Page', text='This is the results page')
 
# Home Page for the user
# @app.route("/home")
# def home():


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")