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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) ######double check 'user.id' if issues

    def __init__(self, title, entry, owner_id): 
        self.title = title
        self.entry = entry
        self.owner_id = owner_id

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True) 
        username = db.Column(db.String(120))
        password = db.Column(db.String(20))
        blogs = db.relationship('Blog', backref='user') #was 'user.id'

def __init__(self, username, password): #got error so i deleted indention?
    self.username = username
    self.password = password

@app.route("/", methods=["GET"])
def index():
    return redirect('/blog') 
 
@app.route("/index", methods=["GET"])
def authors():
    authors=User.query.all() 
    author_id = request.args.get('id') 
    if author_id: 
        author_blog = Blog.query.get(author_id)
        return render_template('index.html', title=author_blog.title, entry=author_blog.entry) 
    
    # return render_template('blog.html', blogs=all_blogs) #title="Build A Blog", posts=Blog.query.filter_by().all())


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        #existing_user = User.query.filter_by(username = session['username']).one() #gets keyerror for user
        existing_user = User.query.filter_by(username = username).one() #gets Multiple rows were found for, goes through if switched to 'all()'
        if username == existing_user: #might not be correct syntax 
            flash ("User name already exists") 
            return redirect('/signup') 
        elif len(username) < 3: 
            flash ("Username must be greater than 3 characters")
            return redirect('/signup') 
        elif len(username) > 20:
            flash ("Username must be less than 20 characters")
            return redirect('/signup') 
        elif len(password) < 3: 
            flash ("Password must be greater than 3 characters")
            return redirect('/signup') 
        elif len(password) > 20:
            flash ("Password must be less than 20 characters")
            return redirect('/signup')   
        elif not password==verify:
            flash ("Password confirmation does not match password")
            return redirect('/signup') 
        else: 
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username 
            url="/index?=" +str(new_user.id)
            return redirect('/newpost')  #return redirect('/login')
    else:
        return render_template ("signup.html") 

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        user = User.query.filter_by(username=username).first() #double check this query, maybe not filter by?  
        if user and user.password == password:
            session['username'] = username
            flash('logged in')
            return redirect("/newpost") 
        elif user is None:
            flash ('enter a user name', 'error')
            return redirect("/login")
        if user is not None and user.username==request.form['username']: #had 'ERROR NoneType' object has no attribute 'username'
            flash('user already exists', 'error')
            return redirect("/login")
        if password is not None and password != user.password: 
            flash('password is not correct', 'error')
            return redirect("/login")
    return render_template("login.html")

@app.before_request
def require_login():
    allowed_routes = ['login','signup', 'index', 'newpost'] #double check 'list_blogs'
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login') 

@app.route('/logout', methods=["GET"])  
def logout():
    del session['username']
    return redirect ("/")

@app.route("/newpost", methods=["POST", "GET"]) 
def newpost(): 
    if request.method == 'POST':
        title=request.form["blog_title"]
        entry=request.form["blog_entry"]
        owner_id=User.query.filter_by(username=session['username']).all() 
        #owner_id=request.form["blog_owner_id"] #throwing up errors 
        
        if title =="": 
            flash("Please enter title for blog post", "error")
            return render_template("newpost.html") 

        if entry=="":
            flash("Please create entry for blog", "error") 
            return render_template("newpost.html") 

        else:
            full_blog = Blog(title=title, entry=entry, owner_id=owner_id) 
            db.session.add(full_blog)
            db.session.commit() ###

           
            return redirect('/blog') #??? adds index to each blog post
    
    return render_template ("newpost.html") 

if __name__ == '__main__':
    app.run()