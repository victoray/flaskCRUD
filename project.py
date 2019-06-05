from flask import Flask, request, redirect, url_for, flash, get_flashed_messages, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine


def start():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def close(session):
    session.close()


@app.route('/')
def home():
    session = start()
    test = session.query(Restaurant).all()

    close(session)
    return render_template('index.html', restaurants=test)

@app.route('/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    session = start()

    rest = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()

    if request.method == 'POST':
        rest.name = request.form['name']
        session.commit()
        return redirect(url_for('home'))

    close(session)
    return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=rest)

@app.route('/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):

    session = start()
    rest = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()

    if request.method == 'POST':
        session.delete(rest)
        session.commit()
        return redirect(url_for('home'))

    close(session)
    return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=rest, item=rest)



@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    session = start()

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
    close(session)
    return render_template('menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)


# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    session = start()

    if request.method == 'POST':
        new_menuitem = MenuItem(name=str(request.form['name']).title(), description=str(request.form['description']),
                                price=(str(request.form['price'])), restaurant_id=restaurant_id)
        print(new_menuitem.name)
        session.add(new_menuitem)
        session.commit()
        close(session)
        flash("new menu item created")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    close(session)
    return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    session = start()

    menu = session.query(MenuItem).filter(MenuItem.id == menu_id).one()

    if request.method == 'POST':
        menu.name = str(request.form['name']).title()
        menu.price = price = ("$" + str(request.form['price']))
        menu.description = str(request.form['description'])
        print(menu.name)
        session.commit()
        close(session)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    close(session)
    return render_template("editmenuitem.html", restaurant_id=restaurant_id, menu_id=menu_id, item=menu)


# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = start()

    menuitem = session.query(MenuItem).filter(MenuItem.id == menu_id).one()

    if request.method == 'POST':
        session.delete(menuitem)
        session.commit()
        close(session)
        flash('Item deleted')
        test = get_flashed_messages()
        print(test)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    close(session)
    return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=menuitem)


if __name__ == '__main__':
    app.secret_key = 'key'
    app.debug = True
    app.run(host="localhost", port=9999)
