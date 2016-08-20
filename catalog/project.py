from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db import Base, Category, Item
from flask import session as login_session
import random
import string

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
    return render_template('catalog.html',
                            categories=categories, 
                            items=items)

@app.route('/catalog/new', methods=['POST','GET'])
def newCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        flash('New Category %s Successfuly Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')

@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategories(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    editCategories = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editCategories.name = request.form['name']
            flash('Category Successfully Edited %s' % editCategories.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', 
                                categories=categories, 
                                category=editCategories)

@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategories(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    deleteCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(deleteCategory)
        flash('%s Successfully Deleted' % deleteCategory.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteCategory.html', 
                                category=deleteCategory,
                                categories=categories)

@app.route('/catalog/<int:category_id>/')
def showItems(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).order_by(Item.name.desc()).filter_by(id=category_id)
    return render_template('items.html', 
                            item=item, 
                            category=category, 
                            categories=categories)

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
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       price = request.form['price'],
                       image=request.form['image'],
                       category_id=category_id)
        session.add(newItem)
        flash('New item %s successfuly added' % newItem.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['POST','GET'])
def editItem(category_id,item_id):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(id=category_id).one()
    editItem = session.query(Item).filter_by(id=item_id).one()
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
        flash('%s Item Successfully Edited' %editItem.name)
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
    if request.method == 'POST':
        session.delete(deleteItem)
        flash('%s Successfully Deleted' % deleteItem.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteItem.html', 
                                item=deleteItem,
                                category_id=category_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)