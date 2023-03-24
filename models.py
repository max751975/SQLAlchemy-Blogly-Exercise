"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# DEFAULT_IMAGE_URL ="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg"

# DEFAULT_IMAGE_URL ="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfnDjz5oIxdzUm27tcvgCtKrwYRqsD3SrL_A&usqp=CAU"

DEFAULT_IMAGE_URL ="https://www.pngkey.com/png/full/170-1709536_user-icon.png"

class User(db.Model):
    """User model"""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    
    first_name = db.Column(db.Text, nullable = False)
    
    last_name = db.Column(db.Text, nullable = False)
    
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)
    
    post = db.relationship("Post", backref='user')
    
    @property
    def full_name(self):
        """Full name of the user"""
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """Post Model"""
    
    __tablename__ = 'posts'
        
    id = db.Column(db.Integer, primary_key = True)
    
    title = db.Column(db.Text, nullable = False)
    
    content = db.Column(db.Text, nullable = False)
    
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.datetime.now)
        
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
    @property
    def short_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%b %-d  %Y")

def connect_db(app):
    db.app = app
    db.init_app(app)