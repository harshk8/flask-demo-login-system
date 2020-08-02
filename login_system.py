from flask import Flask, request, redirect, render_template, url_for, session
# from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import bcrypt


#Mongo DB connection
client = MongoClient("mongodb+srv://dexter:JCwAFG3Cliub7vCm@cluster0.4ndko.mongodb.net/dexter_db?retryWrites=true&w=majority")
db = client.get_database('dexter_db')
records = db.dexter_collection
records.count_documents({})

app = Flask(__name__)
 
@app.route('/', methods=['GET'])
def index():
    username = 'DAUMMY' 
    if 'username' in session:
        username = session['username']
    return render_template('index.html', username=username)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method=='POST':
        exist_user = records.find_one(
            {'name': request.form['username']})
        if not exist_user:
            encrypt_pass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            records.insert_one({
                'name': request.form['username'],
                'password': encrypt_pass
                })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'user with this username already exist.'
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method=='POST':
        exist_user = records.find_one({'name': request.form['username']})
        if exist_user:
            if bcrypt.checkpw(
                request.form['password'].encode('utf-8'),
                exist_user['password']
                ):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        return 'Entered credentials are wrong.'
    return render_template('login.html')


if __name__=='__main__':
    app.secret_key = 'itissceret'
    app.run(debug=True)