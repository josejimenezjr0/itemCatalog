from flask import Flask, render_template, url_for, request, redirect, flash,\
    jsonify
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import User, Category, Item, Base
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5432/itemCatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        print("entered if request.args.get('state') != login_session['state']:")
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print login_session
    print "done!"
    return output

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Show all Categories
@app.route('/')
def homePage():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(desc(Item.id)).limit(5).all()
    if 'username' not in login_session:
        return render_template('publicItemsCatalog.html', categories=categories, items=items)
    else:
        return render_template('ItemsCatalog.html', categories=categories, items=items)

@app.route('/catalog/<category_Name>/')
def itemsList(category_Name):
    category = session.query(Category).filter_by(name=category_Name).one()
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).filter_by(
        category_id=category.id).all()
    if 'username' not in login_session:
        return render_template('publicItemsList.html', items=items, categoryOne=category, categories=categories)
    else:
        return render_template('itemsList.html', items=items, categoryOne=category, categories=categories)

@app.route('/catalog/<category_Name>/<item_Name>/')
def item(category_Name, item_Name):
    category = session.query(Category).filter_by(name=category_Name).one()
    item = session.query(Item).filter_by(name=item_Name).one() 
    creator = getUserInfo(item.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicItem.html', item=item)
    else:
        return render_template('item.html', item=item)

@app.route('/catalog/<category_Name>/<item_Name>/edit', methods=['GET', 'POST'])
def editItem(category_Name, item_Name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_Name).one()
    categories = session.query(Category).order_by(asc(Category.name))
    editedItem = session.query(Item).filter_by(name=item_Name).one()
    if login_session['user_id'] != editedItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this item.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            cat = request.form['category']
            editCategory = session.query(Category).filter_by(name=cat).one()
            editedItem.category_id = editCategory.id
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited')
        return redirect(url_for('itemsList', category_Name=category.name))
    else:
        return render_template('editItem.html', item=editedItem, categoryOne=category.name, categories=categories)

@app.route('/catalog/<category_Name>/<item_Name>/delete', methods=['GET', 'POST'])
def deleteItem(category_Name, item_Name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_Name).one()
    categories = session.query(Category).order_by(asc(Category.name))
    itemToDelete = session.query(Item).filter_by(name=item_Name).one()
    if login_session['user_id'] != itemToDelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this item.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Category Item Successfully Deleted')
        return redirect(url_for('itemsList', category_Name=category.name))
    else:
        return render_template('deleteItem.html', item=itemToDelete, categoryOne=category.name)

@app.route('/catalog/new/', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        cat = request.form['category']
        newCatItem = session.query(Category).filter_by(name=cat).one()
        newItem = Item(
            name = request.form['name'],
            description = request.form['description'],
            user_id=login_session['user_id'],
            category_id = newCatItem.id)
        session.add(newItem)
        session.commit()
        flash('Category Item Successfully Added')
        return redirect(url_for('homePage'))
    else:
        return render_template('addItem.html', categories=categories)

@app.route('/JSON')
def catalogJSON():
    catList = session.query(Category).all()
    catalog = {}
    catalog['categories'] = []
    for i in catList:
        catSerial = i.serialize
        itemList = session.query(Item).filter_by(category_id=i.id)
        catSerial['items'] = []
        for j in itemList:
            catSerial['items'].append(j.serialize)
        catalog['categories'].append(catSerial)
    return jsonify(catalog)
        

# Disconnect
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('homePage'))
    else:
        flash("You were not logged in")
        return redirect(url_for('homePage'))


if __name__ == '__main__':
    app.secret_key = 'super_duper_extra_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)