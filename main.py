from flask import Flask, request, redirect, render_template, session, flash
from app import app, db, is_email
from models import User, Blog

@app.route("/login", methods=['GET', 'POST'])
def login():
    #if req method is post the user has filled out the form and now its being validated
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.username
                flash('welcome back, '+user.username)
                return redirect("/")
        flash('bad username or password', category='error')
        return redirect("/login")
    #if req method is get it means its your first time to the page
    else:
        return render_template('login.html')

@app.route("/logout", methods=['GET'])
#had to use post bc links
def logout():
    del session['user']
    return redirect("/")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #username validation
        username = request.form['username']
        username_error = ''
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            username_error = f'Oops! {username} has been taken!'
        elif username == '':
            username_error = "Enter a username!"
            username = ''
        elif ' ' in username or len(username) < 3 or len(username) > 20:
            username_error = "Username is not valid! username must be 3-20 characters and cannot contain a space or special characters."
            username = ''
        #password validation
        password = request.form['password']
        password_error = ''
        if password == '':
            password_error = "Enter a password!"
            password == ''
        elif ' ' in password or len(password) < 3 or len(password) > 20:
            password_error = "Password is not valid!"
            password = ''
        #verify validation
        verify = request.form['verify']
        verify_error = ''
        if password != verify:
            verify_error = 'passwords did not match'

        #displays form with errors if there is a error
        if (username_error or password_error or verify_error):
            return render_template('register.html', 
            title='Register',
            username_error=username_error,
            password_error=password_error,
            verify_error=verify_error
            )

        #all error variables are empty. adds user to database and redirects to newpost
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/newpost")

    #request method is GET. returns unmarked register form
    else:
        return render_template('register.html', title='Register')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    #if a blog id is passed into app route it will go here
    blog_id = request.args.get('id')
    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", title=post.title, body=post.body,)
    
    #if a username is passed it goes here
    username = request.args.get('user')
    user = User.query.filter_by(username=username).first()
    if user:
        posts = Blog.query.filter_by(author_id=user.id)
        return render_template('main-page.html', posts=posts, title=f"{user.username} is a chump.")

    #if someone types in /blog it gives an error so now it will just redirect them to main page with an error
    flash("To view /blog click on a user", category='error')
    return redirect ('/')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    #if form was submitted.
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user =  User.query.filter_by(username=session['user']).first()
        #validation that form is not empty
        title_error = ""
        body_error = ""
        if title == "":
            title_error = "Title required."
        if body == "":
            body_error = "Content required."
        #if errors exist it will display form with 'helpful' messages
        if title_error or body_error:
            return render_template("new-post.html",
                title = title,
                body = body,
                title_error = title_error,
                body_error = body_error
            )
        else:
            #validated. stores form data in db
            new_post = Blog(title, body, user)
            db.session.add(new_post)
            db.session.commit()
            page_id = new_post.id
            return redirect(f"/blog?id={page_id}")
    #if request method was GET i want it to display blank form 
    else:
        return render_template('new-post.html', title="New Post")

@app.route("/", methods=['GET'])
def index():
    users = User.query.all()
    return render_template('users.html', users=users, title='blog users!')


#ensures users must log in to see the super secret posts
endpoints_without_login = ['login', 'register']
@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/register")

if __name__ == '__main__':
    app.run()