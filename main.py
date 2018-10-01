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


@app.route("/")
def index():
    return redirect("/blog")

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    print(f'{blog_id}')
    posts = Blog.query.all()

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", title=post.title, body=post.body,)

    return render_template('main-page.html', posts=posts)

@app.route('/newpost')
def post():
    return render_template('new-post.html', title="New Post")

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title = request.form['title']
    body = request.form['body']
    print(body)

    title_error = ""
    body_error = ""

    if title == "":
        title_error = "Title required."

    if body == "":
        body_error = "Content required."


    if not title_error and not body_error:
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()
        page_id = new_post.id
        return redirect(f"/blog?id={page_id}")
    else:
        return render_template("new-post.html",
            title = title,
            body = body,
            title_error = title_error,
            body_error = body_error
        )

    

if __name__ == '__main__':
    app.run()