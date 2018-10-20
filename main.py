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

    def __init__(self, title, entry): 
        self.title = title
        self.entry = entry

@app.route("/", methods=["GET"])
def index():
    return redirect('/blog') 
 
@app.route("/blog", methods=["GET"])
def single_blog():
    #queries all blogs 
    all_blogs=Blog.query.all() 

    #if a request if made for a specific blog id, bring up single blog post
    blog_id = request.args.get('id') 
    if blog_id: 
        single_blog = Blog.query.get(blog_id)
        return render_template('ind_blog_post.html', title=single_blog.title, entry=single_blog.entry) 
    
    return render_template('blog.html', blogs=all_blogs) #title="Build A Blog", posts=Blog.query.filter_by().all())
  
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