from app import db
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(150), nullable=True, default='default.jpg')
    cover_photo = db.Column(db.String(150), nullable=True, default='default_cover.jpg')
    education = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    work_experience = db.Column(db.Text, nullable=True)
    linkedin = db.Column(db.String(250), nullable=True)
    github = db.Column(db.String(250), nullable=True)
    twitter = db.Column(db.String(250), nullable=True)

    # Relationships for connections and posts
    connections = db.relationship('Connection', backref='user', lazy='dynamic', foreign_keys='Connection.user_id')
    connection_requests_sent = db.relationship('ConnectionRequest', backref='requester', lazy='dynamic', foreign_keys='ConnectionRequest.sender_id')
    connection_requests_received = db.relationship('ConnectionRequest', backref='receiver', lazy='dynamic', foreign_keys='ConnectionRequest.receiver_id')
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}, {self.email}>'


# Connection model (Accepted connections)
class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    connection_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Connection {self.user_id} -> {self.connection_id}>'


# ConnectionRequest model
class ConnectionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")  # pending, accepted, declined

    def __repr__(self):
        return f'<ConnectionRequest {self.sender_id} -> {self.receiver_id} (status={self.status})>'


# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.id}, {self.content[:20]}>'


# Comment model (Optional: Extendable for posts)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}, Post {self.post_id}>'


# Like model (Optional: Likes for posts)
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'<Like User {self.user_id} -> Post {self.post_id}>'
