from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db import Base, Category, Item, User
from flask import session as login_session
import random
import string
# stores oauth2 params
from oauth2client.client import AccessTokenCredentials

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).filter_by(category_id=Category.id)
    # Display the newest item on the page
    newestItem = session.query(Item).order_by(Item.id.desc()).filter_by(category_id=Category.id).first()
    return render_template('catalog.html',
                            categories=categories, 
                            items=items,
                            newestItem=newestItem)

# Category CRUD operations
@app.route('/catalog/new', methods=['POST','GET'])
def newCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            newCategory = Category(name=request.form['name'])
            session.add(newCategory)
            flash('New Category \"%s\" Successfuly Created' % newCategory.name)
            session.commit()
            return redirect(url_for('showCategories'))
        else:
            return render_template('newCategory.html')

@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategories(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    editCategories = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            if request.form['name']:
                editCategories.name = request.form['name']
                flash('Category Successfully Edited \"%s\"' % editCategories.name)
                return redirect(url_for('showCategories'))
        else:
            return render_template('editCategory.html', 
                                    categories=categories, 
                                    category=editCategories)

@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategories(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    deleteCategory = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            session.delete(deleteCategory)
            flash('\"%s\" Successfully Deleted' % deleteCategory.name)
            session.commit()
            return redirect(url_for('showCategories', category_id=category_id))
        else:
            return render_template('deleteCategory.html', 
                                    category=deleteCategory,
                                    categories=categories)

@app.route('/catalog/<int:category_id>/')
def showItems(category_id):
    categories = session.query(Category).order_by(Category.name.asc()).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).order_by(Item.name.desc()).filter_by(category_id=category_id).all()
    return render_template('items.html', 
                            categories=categories, 
                            items=items, 
                            category=category)

# Item CRUD operations
@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def itemPage(category_id,item_id):
    categories = session.query(Category).order_by(asc(Category.name))
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html',
                            item=item,
                            category_id=category_id,
                            item_id=item_id,
                            categories=categories)
@app.route('/catalog/<int:category_id>/new', methods=['POST','GET'])
def newItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:    
        if request.method == 'POST':
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           price = request.form['price'],
                           image=request.form['image'],
                           category_id=category_id)
            session.add(newItem)
            flash('New item \"%s\" successfuly added' % newItem.name)
            session.commit()
            return redirect(url_for('showCategories', category_id=category_id))
        else:
            return render_template('newItem.html', category_id=category_id)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['POST','GET'])
def editItem(category_id,item_id):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(id=category_id).one()
    editItem = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            if request.form['name']:
                editItem.name = request.form['name']
            if request.form['description']:
                editItem.description = request.form['description']
            if request.form['price']:
                editItem.price = request.form['price']
            if request.form['image']:
                editItem.image = request.form['image']
            session.add(editItem)
            session.commit()
            flash('\"%s\" Item Successfully Edited' %editItem.name)
            return redirect(url_for('showCategories', item_id=item_id))
        else:
            return render_template('editItem.html',
                                    category_id=category_id, 
                                    item_id=item_id, 
                                    item=editItem, 
                                    categories=categories)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete', methods=['POST','GET'])
def deleteItem(category_id,item_id):
    deleteItem = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            session.delete(deleteItem)
            flash('\"%s\" Successfully Deleted' % deleteItem.name)
            session.commit()
            return redirect(url_for('showCategories', category_id=category_id))
        else:
            return render_template('deleteItem.html', 
                                    item=deleteItem,
                                    category_id=category_id)

# All JSON Functions
# JSON APIs to view Item Information
@app.route('/catalog/<int:category_id>/items/JSON')
def itemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])

# User Login Functions
CLIENT_ID = json.loads(
    open('fb_client_secrets.json', 'r').read())['web']['app_id']
APPLICATION_NAME = "Item Catalog Application"

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
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

    flash("Now logged in as %s" % login_session['username'])
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))
# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], 
                   email=login_session['email'], 
                   picture=login_session['picture'])
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


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)