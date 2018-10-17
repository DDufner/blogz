from flask import Flask, request, redirect, render_template, session, flash
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
    entry = db.Column(db.Text)

    def __init__(self, title, entry): #check on how to pass through multiple things
        self.title = title
        self.entry = entry
        #self.owner=owner

#blogs =[]

@app.route('/', methods=['POST', 'GET'])
def index():
    #below might need to be redone to direct between pages.  
    if request.method == 'POST':
        new_blog = request.form['blog_title']
        new_blog = Blog(new_blog)
        db.session.add(new_blog)
        db.session.commit()
    blogs = Blog.query.all()
    return render_template('blog.html', name="blog_title", blogs=blogs) #add part to render blog posts) 
    # blogs = Blog.query.filter_by(completed=False).all() 
    # completed_blogs = Blog.query.filter_by(completed=True).all()
   # return render_template('todos.html',title="Get It Done!", 
       # tasks=tasks, completed_tasks=completed_tasks)

# @app.route('/blog/<int:blog_id>') #default method is GET
# def blog(blog_id):
#     blog=Blog.query.filter_by(id=blog_id).one()
#     return render_template('blog.html', blog=blog)

@app.route("/", methods=["GET"])
def return_to_main():
    return render_template ('/blog')

@app.route('/newpost', methods=["POST"])
def newpost():
    title=request.form["blog_title"]
    entry=request.form["blog_entry"]
    new_blog_template = jinja_env.get_template ("newpost.html")
    if request.method == 'POST':
        if title =="":
            blog_title_error="Please enter title for blog post"
            return new_blog_template.render()
        else:
            entry ==""
            blog_entry_error="Please make blog entry"  
            return new_blog_template.render()
    else:
        return new_blog_template.render()  
        
    post=Blog(blog_title=blog_title, blog_date=blog_date, blog_entry=blog_entry)

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('blog')) ## 
    #return '<h1>title: {} date: {} entry: {}</h1>'.format(title, date, entry) 
    #return render_template('newpost.html')

#NOTE: below is just for learning/ref, not needed
@app.route('/delete_blog', methods=["POST"])
def delete_blog():
    blog_id = int(request.form["blog-id"])
    blog =Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect('/')
# @app.route('/', methods=["GET", "POST"])
# def index(): 
#     blog = Blog.query.all()
#     return redirect ("/blog")#render_template('blog.html') #last error 

if __name__ == '__main__':
    app.run()