from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from libraries.date import get_date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()

@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)


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
    title = db.Column("title", db.String(250))
    author = db.Column("Author", db.String(100))
    date = db.Column("Date", db.String(100))
    content = db.Column(db.Text, nullable=False)


@app.route('/new_entry/', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        date = get_date()
        content = request.form['content']
        new_post = BlogPost(author=author, title=title, date=date, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('archives'))
    return render_template('new_entry.html')


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
