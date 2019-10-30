from flask import Flask, render_template, request, redirect, url_for, session, \
    flash
from warrant import Cognito
from settings import *
from botocore.exceptions import ClientError

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
u = Cognito(USER_POOL_ID, CLIENT_ID, user_pool_region=REGION)


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('user_login') is True:
        u = Cognito(USER_POOL_ID, CLIENT_ID, REGION,
                    id_token=session.get('id_token'),
                    refresh_token=session.get('refresh_token'),
                    access_token=session.get('access_token'),
                    username=session.get('username'))

        return render_template("index.html", username=u.username,
                               user_login=session.get('user_login'))

    return render_template('index.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == "POST":

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # hashed in warrant
        password_confirm = request.form['confirm_password']
        if password != password_confirm:
            flash("Passwords don't match!")
            return redirect(url_for('signup'), code=307)
        u.add_base_attributes(email=email)
        try:
            u.register(username, password)
            return redirect(url_for("confirm_signup", username=username))
        except ClientError as e:
            flash(e.response.get('Error').get('Message'))

    return render_template("signup.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    # TODO: render to each user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = Cognito(USER_POOL_ID, CLIENT_ID, REGION, username=username,
                    access_key='dummy_not_used', secret_key='dummy_not_used')

        try:
            u.authenticate(password)
            session['asscess_token'] = u.access_token
            session['refresh_token'] = u.refresh_token
            session['id_token'] = u.id_token
            session['user_login'] = True
            session['username'] = username
            return redirect(url_for('index'))
        except ClientError as e:
            flash(e.response.get('Error').get('Message'))

    return render_template("login.html")


@app.route('/confirm_signup/<username>', methods=['GET','POST'])
def confirm_signup(username):
    if request.method == 'POST':
        code = request.form['confirm_code']
        u = Cognito(USER_POOL_ID, CLIENT_ID, REGION, username=username,
                    access_key='dummy_not_used', secret_key='dummy_not_used')
        try:
            u.confirm_sign_up(code, username=username)
        except ClientError as e:
            flash(e.response.get('Error').get('Message'))
            return redirect(url_for('confirm_signup', username=username))
        return redirect(url_for('login', username=username))

    return render_template('confirm_signup.html')


@app.route('/logout')
def logout():
    if session.get('user_login'):
        session.clear()
    return render_template('index.html')


# @app.route('/confirm_signup')
# def confirm():
#     return render_template('confirm_signup.html')


if __name__ == '__main__':
    app.run(debug=True)
