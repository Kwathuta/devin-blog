from flask import render_template, redirect, url_for, abort, request
from . import main
from flask_login import login_required, current_user
from ..models import User, Blog, Comment, Like, Dislike
from .forms import UpdateProfile, BlogForm, CommentForm
from .. import db, photos
from ..requests import get_quotes


@main.route("/")
def index():
    blogs = Blog.query.all()
    lifestyle = Blog.query.filter_by(category="Lifestyle").all()
    fitness = Blog.query.filter_by(category="Fitness").all()
    diy = Blog.query.filter_by(category="DIY").all()
    quotes = get_quotes()
    return render_template(
        "index.html",
        blogs=blogs,
        lifestyle=lifestyle,
        fitness=fitness,
        diy=diy,
        quotes=quotes,
    )


@main.route("/new_blog", methods=["GET", "POST"])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_blog_object = Blog(
            post=post,
            user_id=current_user._get_current_object().id,
            category=category,
            title=title,
        )
        new_blog_object.save_blog()
        return redirect(url_for("main.index"))

    return render_template("new_blog.html", form=form)


@main.route("/comments/<int:blog_id>", methods=["POST", "GET"])
@login_required
def comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    all_comments = Comment.query.filter_by(blog_id=blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment=comment, user_id=user_id, blog_id=blog_id)
        new_comment.save_comment()
        return redirect(url_for(".comment", blog_id=blog_id))
    return render_template(
        "comment.html", form=form, blog=blog, all_comments=all_comments
    )


@main.route("/user/<name>")
def profile(name):
    user = User.query.filter_by(username=name).first()
    user_id = current_user._get_current_object().id
    posts = Blog.query.filter_by(user_id=user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, posts=posts)


@main.route("/user/<name>/updateprofile", methods=["POST", "GET"])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username=name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for(".profile", name=name))
    return render_template("profile/update.html", form=form)


@main.route("/user/<name>/update/avatar", methods=["POST"])
@login_required
def update_avatar(name):
    user = User.query.filter_by(username=name).first()
    if "photo" in request.files:
        filename = photos.save(request.files["photo"])
        path = f"photos/{filename}"
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for("main.profile", name=name))


@main.route("/like/<int:id>", methods=["POST", "GET"])
@login_required
def like(id):
    get_blogs = Like.get_likes(id)
    valid_string = f"{current_user.id}:{id}"
    for blog in get_blogs:
        to_str = f"{blog}"
        print(valid_string + " " + to_str)
        if valid_string == to_str:
            return redirect(url_for("main.index", id=id))
        else:
            continue
    new_like = Like(user=current_user, blog_id=id)
    new_like.save_like()
    return redirect(url_for("main.index", id=id))


@main.route("/dislike/<int:id>", methods=["POST", "GET"])
@login_required
def dislike(id):
    blog = Dislike.get_dislikes(id)
    valid_string = f"{current_user.id}:{id}"
    for i in blog:
        to_str = f"{i}"
        print(valid_string + " " + to_str)
        if valid_string == to_str:
            return redirect(url_for("main.index", id=id))
        else:
            continue
    new_dislike = Dislike(user=current_user, blog_id=id)
    new_dislike.save_dislike()
    return redirect(url_for("main.index", id=id))
