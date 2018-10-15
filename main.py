from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 

app=Flask (__name__)
app.config["DEBUG"]=True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='RR247a'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post_date = db.Column(db.DateTime)
    entry = db.Column(db.Text)

    def __init__(self, name): 
        self.title = title
        self.entry = entry
        #self.owner=owner

blogs =[]

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_blog = request.form['blog_title'] #new post?  
        new_blog = Blog(new_blog)
        db.session.add(new_blog)
        db.session.commit()
    return render_template('blog.html') #add part to render blog posts) 
    # blogs = Blog.query.filter_by(completed=False).all() 
    # completed_blogs = Blog.query.filter_by(completed=True).all()
   # return render_template('todos.html',title="Get It Done!", 
       # tasks=tasks, completed_tasks=completed_tasks)

# @app.route('/blog/<int:blog_id>') #default method is GET
# def blog(blog_id):
#     blog=Blog.query.filter_by(id=blog_id).one()
#     return render_template('blog.html', blog=blog)
 
@app.route('/newpost', methods=["POST"])
def newpost():
    title=request.form["blog_title"]
    date=request.form["blog_date"]
    entry=request.form["blog_entry"]
    post=Blog(blog_title=blog_title, blog_date=blog_date, blog_entry=blog_entry)

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('blog')) ##
    #return '<h1>title: {} date: {} entry: {}</h1>'.format(title, date, entry) 
    #return render_template('newpost.html')

# @app.route('/', methods=["GET", "POST"])
# def index(): 
#     blog = Blog.query.all()
#     return redirect ("/blog")#render_template('blog.html') #last error 

if __name__ == '__main__':
    app.run()