from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True     
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


def get_blog_posts():
    Blogs = Blog.query.all()
    return Blogs

@app.route('/blog', methods=['POST', 'GET'])
def index():
    return render_template('main-page.html', blogs=get_blog_posts())


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        title_error = ''
        if title == '':
            title_error = 'Title cannot be empty!'

        body = request.form['body']
        body_error = ''
        if body == '':
            body_error = 'Body cannot be empty!'
        
        if not body_error and not title_error:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
        return render_template('new-post.html',
            body_error = body_error,
            title_error = title_error)

    return render_template('new-post.html')
    
    


if __name__ == '__main__':
    app.run()