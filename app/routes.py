''' routes.py file '''
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres1234',
    'db': 'blogpost',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route("/")
def blog():
    posts = Blogpost.query.all()

    return render_template('articles.html', posts=posts)

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/contact/")
def contact():
    return render_template('contact.html')

@app.route("/post/<int:pk>")
def post(pk):
    post = Blogpost.query.filter_by(id=pk).one()

    date_posted = post.date_posted.strftime('%B %d, %Y at %I:%M:%S %p')

    return render_template('post.html', post=post, date_posted=date_posted)

@app.route("/add/")
def add():
    return render_template('add.html')

@app.route("/addpost", methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('blog'))

if __name__ == "__main__":
    app.run(debug=True)
