"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# DEFAULT_IMAGE_URL ="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg"

DEFAULT_IMAGE_URL ="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfnDjz5oIxdzUm27tcvgCtKrwYRqsD3SrL_A&usqp=CAU"

class User(db.Model):
    """User model"""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    
    first_name = db.Column(db.Text, nullable = False)
    
    last_name = db.Column(db.Text, nullable = False)
    
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)
    
    @property
    def full_name(self):
        """Full name of the user"""
        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    db.app = app
    db.init_app(app)