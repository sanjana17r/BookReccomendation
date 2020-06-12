from flask import Flask,render_template,request,jsonify,redirect,url_for
from flask_mysqldb import MySQL
import numpy as np # linear algebra
import pandas as pd
from bookrec import authors_recommendations,corpus_recommendations,totgenre,genre_based,books

app = Flask(__name__)
books = pd.read_csv(r'C:\sanju\nptel\booksRec\templates\all.csv', encoding = "UTF-8")
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        k=request.form['title']
        return redirect(url_for('index',ty=k))      
    else:
        return render_template("index.html",bname=(books['name.1']),totgenre=totgenre)
        


@app.route('/<genre>',methods=['GET','POST'])
def gen(genre):
    if request.method=='GET':
        k=genre_based(genre)
        return render_template("imp.html",names=list(k[0]),links=list(k[1]),iim=list(k[2]),autho=list(k[3]),totgenre=totgenre,headd=genre)   
    else:
        return render_template('index.html',totgenre=totgenre)



@app.route('/books/yes/<ty>',methods=['GET','POST'])
def index(ty):
    if request.method=='GET':
        k=(corpus_recommendations(ty))
        return render_template("imp.html",names=list(k[0]),links=list(k[2]),iim=list(k[1]),autho=list(k[3]),totgenre=totgenre,headd='Recommendations :')  
    else:
        print(list(books['name.1']))
        return render_template('index.html',totgenre=totgenre)    

@app.route('/Authors')
def authors():
    return render_template('norm.html',totauthor=list(set(books['author'])),totgenre=totgenre)  

@app.route('/About')
def about():
    return render_template('norm.html',totauthor=['This is a website for book reccomendation (based on Machine Learning using python), and backend done using flask.'],totgenre=totgenre) 

@app.route("/tut", methods=["POST", "GET"])
def tut():
    return render_template("imgslider.html")



if __name__ == "__main__":
    app.run(debug=True)