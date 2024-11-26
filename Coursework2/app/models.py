from app import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(150), nullable=True, default='default.jpg')

    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    connections = db.relationship(
        'Connection',
        backref='user',
        primaryjoin="or_(User.id == Connection.user_id, User.id == Connection.connection_id)",
        lazy=True
    )

    # Set password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    # Check password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Connection model
class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    connection_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
