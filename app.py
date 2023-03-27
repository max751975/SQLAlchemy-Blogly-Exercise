"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, Post, User, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    # posts = Post.query.all()
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("/posts/homepage.html", users=users, posts=posts)

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
    posts = Post.query.filter(Post.user_id==user_id).order_by(Post.created_at.desc()).limit(5).all()
    return render_template('users/show_user.html', user=user, posts=posts)

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
# ---------------------------------------------------------------------
#  Routes for posts

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show page with post info"""

    post = Post.query.get_or_404(post_id)
    # posts = Post.query.filter(Post.user_id==user_id)
    return render_template('posts/show_post.html', post=post)

@app.route('/users/<int:user_id>/posts')
def user_all_posts(user_id):
    """Show all posts for user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id==user_id).order_by(Post.created_at.desc()).all()
    return render_template("/posts/user_all_posts.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def new_post_form(user_id):
    """Show form to add new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("/posts/new_post.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    """Handle form to add new post"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=request.form['title'], content=request.form['content'], user_id=user_id, tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f"/users/{user.id}")

@app.route('/posts/<int:post_id>/edit')
def post_edit(post_id):
    """Show a form to edit post with given id"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_delete(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/")

# -----------------------------------------------------------------
# routes for tags

@app.route('/tags')
def show_all_tags():
    """Show all tags"""
    tags = Tag.query.all()
    return render_template("/tags/show_all_tags.html", tags = tags)

@app.route('/tags/new', methods=['GET'])
def new_tag_form():
    """Form to create new tag"""
    return render_template('/tags/new_tag.html')

@app.route("/tags/new", methods=['POST'])
def new_tag():
    """Get data for new tag from the form and create new tag"""
    
    new_tag = Tag(name = request.form['name'])
    
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show page with tag info"""

    tag = Tag.query.get_or_404(tag_id)
    # posts = Post.query.filter(Post.user_id==user_id)
    return render_template('tags/show_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tag_edit(tag_id):
    """Show a form to edit tag with given id"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tag_update(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
   
    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tag_delete(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")