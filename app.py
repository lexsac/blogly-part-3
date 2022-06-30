"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    """Redirects to list of users."""

    return redirect("/users")

#########################
# User routes

@app.route("/users")
def list_users():
    """List users."""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def new_user_form():
    """Form for adding a new user."""

    return render_template("users_new.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Form for adding a new user."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show form to edit a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def submit_edited_user(user_id):
    """Show form to edit a single user."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a single user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

#########################
# Post routes

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show form to add a post for a single user."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("posts_new.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Handle add form; add post and redirect to user detail page."""

    user = User.query.get_or_404(user_id)
    
# I don't understand these two lines...
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""

    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_posts(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    
    return render_template('post_edit.html', post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_edited_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

# I don't understand these two lines...
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a single post."""

    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

#########################
# Tag routes

@app.route("/tags")
def show_tags():
    """Lists tags."""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show a tag. Show buttons to edit and delete the tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)

@app.route("/tags/new")
def new_tag_form():
    """Form for adding a new tag."""

    posts = Post.query.all()
    return render_template("tags_new.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def add_new_tag():
    """Form for adding a new tag."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()   
    
    name = request.form['name']

    tag = Tag(name=name, posts=posts)
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tags(tag_id):
    """Show form to edit a tag, and to cancel (back to tags page)."""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tag_edit.html', tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def submit_edited_tag(tag_id):
    """Show form to edit a tag, and to cancel (back to tags page)."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a single tag."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")