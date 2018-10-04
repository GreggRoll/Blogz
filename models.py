from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user
    
    def __repr__(self):
        return f'{self.title}'