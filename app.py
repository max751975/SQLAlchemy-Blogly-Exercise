"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect("/users")

@app.route('/users')
def user_list():
    """Shows a list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("/users/index.html", users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    """Form to create new user"""
    return render_template('/users/new.html')

@app.route("/users/new", methods=['POST'])
def new_user():
    """Get data for new user from the form and create new user"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show page with user's info"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show_user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit a user with given id"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def user_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")    

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")