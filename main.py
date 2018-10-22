from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app=Flask (__name__)
app.config["DEBUG"]=True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hell0@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
app.secret_key='RR247a'

class Blog(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(120)) 
    entry = db.Column(db.Text) 
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) ######double check 

    def __init__(self, title, entry): 
        self.title = title
        self.entry = entry
        self.owner = owner

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True) 
        username = db.Column(db.String(120))
        password = db.Column(db.String(20))
        blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password): #got error, deleted indentation?
        self.username = username
        self.password = password

#### Still need to initialize tables, #####
#### ! getting error when i try to 'db.create_all()'


@app.route("/", methods=["GET"]) #double check
def index():
    return redirect('/blog') 
 
# @app.route("/blog", methods=["GET"])
# def single_blog():
#     #queries all blogs 
#     all_blogs=Blog.query.all() 

    #if a request if made for a specific blog id, bring up single blog post
    blog_id = request.args.get('id') 
    if blog_id: 
        single_blog = Blog.query.get(blog_id)
        return render_template('ind_blog_post.html', title=single_blog.title, entry=single_blog.entry) 
    
    return render_template('blog.html', blogs=all_blogs) #title="Build A Blog", posts=Blog.query.filter_by().all())
  
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        if username = existing_user: #might not be correct syntax 
            flash ("User name already exists")
            return render_template('/signup') 
        elif len(username) < 3: 
            flash ("Must be greater than 3 characters")
            return render_template('/signup') 
        elif len(username) > 20:
            flash ("Must be less than 20 characters")
            return render_template('/signup') 
        elif len(password) < 3: 
            flash ("Must be greater than 3 characters")
            return render_template('/signup') 
        elif len(password) > 20:
            flash ("Must be less than 20 characters")
            return render_template('/signup')   
        elif not password==confirmation:
            flash ("Password confirmation does not match password")
            return render_template('/signup') 
        
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username 
            return redirect('/newpost')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html') ##


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('logged in')
            return redirect("/newpost") 
        elif not user == user.username:
            flash('user does not exist', 'error')
            return redirect("/login")
        elif not password == user.password:
            flash('password is not correct', 'error')
            return redirect("/login")
    return render_template("login.html")

@app.before_request
def require_login():
    allowed_routes = ['login','signup', 'index', 'list_blogs'] #double check 'list_blogs'
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login') 

@app.route() ##
def logout():
    del session['username']
    return redirect ("/blog")

@app.route("/newpost", methods=["POST", "GET"]) 
def newpost(): 
    if request.method == 'POST':
        title=request.form["blog_title"]
        entry=request.form["blog_entry"]
        
        if title =="": 
            flash("Please enter title for blog post", "error")
            return render_template("newpost.html") 
        if entry=="":
            flash("Please create entry for blog", "error") 
            return render_template("newpost.html") 
            #terminating after this else if
            # entry ==""
            # flash("Please make blog entry", "error") 

        else:
        # needs to not send to DB if incorrect.  
            full_blog = Blog(title, entry)
            db.session.add(full_blog)
            db.session.commit()

            url= "/blog?=" + str(full_blog.id)                    
            return redirect(url) #??? adds index to each blog post
    
    return render_template ("newpost.html") 

if __name__ == '__main__':
    app.run()