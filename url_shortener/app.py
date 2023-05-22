from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Urls(db.Model):
    id_=db.Column("id_",db.Integer,primary_key=True)
    long = db.Column("long",db.String())
    short = db.Column("short",db.String(3))

    def __init__(self,long,short):
        self.long=long
        self.short=short

with app.app_context():
    db.create_all()

def shorten_url():
    letters=string.ascii_letters
    while(True):
        rand_letters=''.join(random.choices(letters,k=3))
        short_url=Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route('/',methods=['POST','GET'])
def home():
    if request.method == "POST":
        url_received = request.form["url"]
        found_url= Urls.query.filter_by(long=url_received).first()
        if(found_url):
            return redirect(url_for("display_short_url",url=found_url.short))
        
        else:
            short_url=shorten_url()
            new_url=Urls(url_received,short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url",url=short_url))
    return render_template('home.html')

@app.route("/display/<url>")
def display_short_url(url):
    return render_template('shorturl.html',short_url_display=url)

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
   url= Urls.query.filter_by(short=short_url).first()
   if url:
        return redirect(url.long)
   else:
        return f'<h1>Url doesnt exist'


if __name__=='__main__':
    app.run(port=5000,debug=True)