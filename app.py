from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from constants import blog_writers

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()

@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)


@app.route('/entry2/')
def entry2():
    return render_template('entry2.html')


@app.route('/archives/')
def archives():
    posts = BlogPost.query.all()
    print(posts)
    return render_template('archives.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post)

class BlogPost(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(100))
    author = db.Column("Number of Posts", db.Integer)
    content = db.Column(db.Text, nullable=False)


@app.route('/new_entry/', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(author=author, title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('archives'))
    return render_template('new_entry.html')


class contributors(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    posts = db.Column("Number of Posts", db.Integer)

    def __init__(self, name, email, posts):
        self.name = name
        self.email = email
        self.posts = posts

def create_contributers(writers):
    for writer in writers:
        found_writer = contributors.query.filter_by(name=writer).first()
        if found_writer:
            continue
        else:
            writer = contributors(writer, "", 0)
            db.session.add(writer)
            db.session.commit()

def delete_posts():
    posts = BlogPost.query.all()
    for post in posts:
        print(post.title)
        # if "natalist" or "n/a" in post.title:
        #     print("yes we found the one")
        #     db.session.delete(post)
        #     db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)

        db.create_all()
        delete_posts()

    app.run(debug=True)
