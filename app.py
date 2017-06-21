#!/Users/simulations/Desktop/Projects/.virtualenvs/Document-Management-System-Front-End/bin/python
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_wtf import Form
from logging import DEBUG
from dotenv import load_dotenv, find_dotenv
import requests
import os

env = load_dotenv(find_dotenv())
api_url = os.getenv("API_URL")
print(api_url)
r = requests.get(api_url)

print (r.json(), type(r.json()))

app = Flask(__name__)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
app.logger.setLevel(DEBUG)
app.secret_key = 'some_secret'

# session['logged_in'] = False

@app.route("/")
def base():
    return render_template("base.pug")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    session['logged_in'] = False
    if request.method == 'POST':
        app.logger.debug('request object: {}'.format(request.form))
        body = {}
        body['firstname'] = request.form['firstname']
        body['lastname'] = request.form['lastname']
        body['username'] = request.form['username']
        body['password'] = request.form['password']
        body['email'] = request.form['email']
        body['departmentId'] = int(request.form['department'])

        app.logger.debug('request object: {}'.format(request.form))
        req = requests.post('{}/users'.format(api_url), data=body)

        print (req.json(), type(req.json()), req.status_code)
        flash(req.json()['message'])

        if int(req.status_code) == 201:
            session['logged_in'] = True
            session['token'] = req.json()['token']
            session['firstname'] = req.json()['data']['firstname']
            session['lastname'] = req.json()['data']['lastname']
            session['email'] = req.json()['data']['email']
            return redirect(url_for('dashboard'))

    session['logged_in'] = False
    return render_template("signup.pug")

@app.route("/login", methods=['GET', 'POST'])
def login():
    session['logged_in'] = False
    if request.method == 'POST':
        body = {}
        body['email'] = request.form['email']
        body['password'] = request.form['password']
        # Logger details to be removed
        app.logger.debug('request object: {}'.format(body))
        req = requests.post('{}/users/login'.format(api_url), data=body)
        print (req)
        try:
            print (req.json(), type(req.json()), req.status_code)
            flash(req.json()['message'])
        except:
            pass
        if int(req.status_code) == 200:
            logged_in = True
            session['token'] = req.json()['token']
            session['firstname'] = req.json()['data']['firstname']
            session['lastname'] = req.json()['data']['lastname']
            session['email'] = req.json()['data']['email']
            session['logged_in'] = True
            return redirect(url_for('dashboard'))

    logged_in = False
    session['logged_in'] = False
    return render_template("login.pug")

@app.route("/dashboard")
def dashboard():
    headers = {'authorization': session.get('token')}
    if not session['logged_in']:
        return redirect(url_for('login'))
    req = requests.get('{}/accesstypes'.format(api_url), headers=headers)
    if req.status_code == 401:
        session['logged_in'] = False
        return redirect(url_for('login'))
    print ('logged in is : ', session['logged_in'])
    return render_template("dashboard.pug", logged_in=session['logged_in'])

@app.route("/accesstypes", methods=["GET", "POST"])
def accesstypes():
    headers = {'authorization': session.get('token')}
    if not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        body = {}
        body['name'] = request.form['access_type_name']
        # Logger details to be removed
        app.logger.debug('request object: {}'.format(body))
        req = requests.post('{}/accesstypes'.format(api_url), data=body, headers=headers)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
        print (req.json()['message'])
    req = requests.get('{}/accesstypes'.format(api_url), headers=headers)
    try:
        # print (req.json(), type(req.json()), req.status_code)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
    except:
        pass
    # print (req.status_code, type(req.status_code))
    return render_template("accesstypes.pug", logged_in=session['logged_in'], req=req, url='{}/accesstypes'.format(api_url))

@app.route("/accesstypes/<id>")
def accesstypes_specific(id):
    headers = {'authorization': session['token']}
    req = requests.delete('{}/accesstypes/{}'.format(api_url, id), headers=headers)
    flash(req.json()['message'])
    if req.status_code == 401:
        session['logged_in'] = False
        return redirect(url_for('login'))
    return redirect(url_for('accesstypes'))
    
@app.route("/roles", methods=["GET", "POST"])
def roles():
    headers = {'authorization': session.get('token')}
    if not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        body = {}
        body['name'] = request.form['role_name']
        # Logger details to be removed
        app.logger.debug('request object: {}'.format(body))
        req = requests.post('{}/roles'.format(api_url), data=body, headers=headers)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
        print (req.json()['message'])
    req = requests.get('{}/roles'.format(api_url), headers=headers)
    try:
        # print (req.json(), type(req.json()), req.status_code)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
    except:
        pass
    # print (req.status_code, type(req.status_code))
    return render_template("roles.pug", logged_in=session['logged_in'], req=req, url='{}/roles'.format(api_url))

@app.route("/roles/<id>")
def roles_specific(id):
    headers = {'authorization': session['token']}
    req = requests.delete('{}/roles/{}'.format(api_url, id), headers=headers)
    flash(req.json()['message'])
    if req.status_code == 401:
        session['logged_in'] = False
        return redirect(url_for('login'))
    return redirect(url_for('roles'))

@app.route("/documenttypes", methods=["GET", "POST"])
def documenttypes():
    headers = {'authorization': session.get('token')}
    if not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        body = {}
        body['name'] = request.form['document_type_name']
        # Logger details to be removed
        app.logger.debug('request object: {}'.format(body))
        req = requests.post('{}/documenttypes'.format(api_url), data=body, headers=headers)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
        print (req.json()['message'])
    req = requests.get('{}/documenttypes'.format(api_url), headers=headers)
    try:
        # print (req.json(), type(req.json()), req.status_code)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
    except:
        pass
    # print (req.status_code, type(req.status_code))
    return render_template("documenttypes.pug", logged_in=session['logged_in'], req=req, url='{}/documenttypes'.format(api_url))

@app.route("/documenttypes/<id>")
def documenttypes_specific(id):
    headers = {'authorization': session['token']}
    req = requests.delete('{}/documenttypes/{}'.format(api_url, id), headers=headers)
    flash(req.json()['message'])
    if req.status_code == 401:
        session['logged_in'] = False
        return redirect(url_for('login'))
    return redirect(url_for('documenttypes'))

@app.route("/departments", methods=["GET", "POST"])
def departments():
    headers = {'authorization': session.get('token')}
    if not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        body = {}
        body['name'] = request.form['department_name']
        # Logger details to be removed
        app.logger.debug('request object: {}'.format(body))
        req = requests.post('{}/departments'.format(api_url), data=body, headers=headers)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
        print (req.json()['message'])
    req = requests.get('{}/departments'.format(api_url), headers=headers)
    try:
        # print (req.json(), type(req.json()), req.status_code)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
    except:
        pass
    # print (req.status_code, type(req.status_code))
    return render_template("departments.pug", logged_in=session['logged_in'], req=req, url='{}/departments'.format(api_url))

@app.route("/departments/<id>")
def departments_specific(id):
    headers = {'authorization': session['token']}
    req = requests.delete('{}/departments/{}'.format(api_url, id), headers=headers)
    flash(req.json()['message'])
    if req.status_code == 401:
        session['logged_in'] = False
        return redirect(url_for('login'))
    return redirect(url_for('departments'))

@app.route("/users", methods=["GET", "POST"])
def users():
    headers = {'authorization': session.get('token')}
    if not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        body = {}
        body['username'] = request.form['user_name']
        
        # Logger details to be removed
        app.logger.debug('request object: {}'.format(body))
        req = requests.post('{}/users/createadmin'.format(api_url), data=body, headers=headers)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
        print (req.json()['message'])
    req = requests.get('{}/users'.format(api_url), headers=headers)
    try:
        # print (req.json(), type(req.json()), req.status_code)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
    except:
        pass
    # print (req.status_code, type(req.status_code))
    return render_template("users.pug", logged_in=session['logged_in'], req=req, url='{}/users'.format(api_url))

@app.route("/users/<id>")
def users_specific(id):
    headers = {'authorization': session['token']}
    req = requests.delete('{}/users/{}'.format(api_url, id), headers=headers)
    flash(req.json()['message'])
    return redirect(url_for('users'))

@app.route("/documents", methods=["GET", "POST"])
def documents():
    headers = {'authorization': session.get('token')}
    if not session['logged_in']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        body = {}
        body['name'] = request.form['document_name']
        # Logger details to be removed
        app.logger.debug('request object: {}'.format(body))
        req = requests.post('{}/documents'.format(api_url), data=body, headers=headers)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
        print (req.json()['message'])
    req = requests.get('{}/documents'.format(api_url), headers=headers)
    try:
        # print (req.json(), type(req.json()), req.status_code)
        flash(req.json()['message'])
        if req.status_code == 401:
            session['logged_in'] = False
            return redirect(url_for('login'))
    except:
        pass
    # print (req.status_code, type(req.status_code))
    return render_template("documents.pug", logged_in=session['logged_in'], req=req, url='{}/documents'.format(api_url))

@app.route("/documents/<id>")
def documents_specific(id):
    headers = {'authorization': session['token']}
    req = requests.delete('{}/documents/{}'.format(api_url, id), headers=headers)
    flash(req.json()['message'])
    if req.status_code == 401:
        session['logged_in'] = False
        return redirect(url_for('login'))
    return redirect(url_for('documents'))
    
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['token'] = None
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
