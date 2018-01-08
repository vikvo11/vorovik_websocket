
#IMPORT MODULES
from misck import token,chat_id_old # Misck.py - config for telegram_bot
    #<Start -Flask modules:>
from flask import jsonify #For response in /webhook
from flask_sslify import SSLify #For use HTTPS
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for,logging #For work with HTTP and templates
from flask_mysqldb import MySQL #For connect to MySQL DB
from HTTP_basic_Auth import auth #For HTTP basic auth
    #<End -Flask modules>
from wtforms import Form, StringField, TextAreaField, PasswordField, validators  # Forms for create HTML fields
from passlib.hash import sha256_crypt # For Password cashing
from functools import wraps # For lock access
#from data import Version
import requests # For HTTP requests
import json # JSON modules
import re # Regular expression - https://pythex.org/

from version import base
from flask_socketio import SocketIO, emit

    #<Start -Declare> :
global kk
kk=0
global last_msg
last_msg=''
#Articles = Articles()
#https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/setWebhook?url=https://vorovik.pythonanywhere.com/
URL='https://api.telegram.org/bot{}/'.format(token)
    #<End -Declare> :
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'morkovka18'
app.debug = True
sslify=SSLify(app)
socketio = SocketIO(app)
#socketio.run(app)


#Config mysql
app.config['MYSQL_HOST']='vorovik.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER']='vorovik'
app.config['MYSQL_PASSWORD']='cb.,fq12-'
app.config['MYSQL_DB']='vorovik$vorovikapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#init MySQL
mysql=MySQL(app)

def write_json(data,filename='answer.json'):
    with open(filename,'w') as f:
        json.dump(data,f,indent=2,ensure_ascii=False)


def get_updates():
    url=URL+'getUpdates'
    r=requests.get(url)
    write_json(r.json())
    return r.json()

def send_message(chatId,text='Please wait a few seconds...!'):
    url=URL+'sendMessage'
    answer = {'chat_id': chatId, 'text': text}
    print(answer)
    r=requests.get(url,json=answer)
    return r.json()

def parc_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern,text).group()
    return crypto[1:]


def get_price(crypto):
    url='https://api.coinmarketcap.com/v1/ticker/{}/'.format(crypto)
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    return price

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
#Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()

@app.route('/angularjs')
def angularjs():
    return render_template('angularjs.html')
    #return 'ok'

@app.route('/deployment',methods=['GET','POST'])
@is_logged_in
def deployment():
    if request.method =='POST':


        k=0
        for i in base:
            #print(i.info)
            base[k].shema=base[k].shema+'1'
            k=k+1
        flash(base[1].shema,'success')
        global kk
        kk=1
        return render_template('deployment.html',articles=base)

    return render_template('deployment.html',articles=base)



#Single articl
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articl
    result = cur.execute("SELECT * FROM articles WHERE id=%s",[id])

    article = cur.fetchone()
    return render_template('article.html',article=article)


#RegisterFormClass
class RegisterForm(Form):
    name = StringField('Name',[validators.length(min=1, max=50)])
    username = StringField('Username',[validators.length(min=4, max=25)])
    email = StringField('Email',[validators.length(min=6, max=50)])
    token = StringField('Token',[validators.length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

#ArticleFormClass
class ArticleForm(Form):
    title = StringField('Title',[validators.length(min=1, max=50)])
    body = TextAreaField('Body',[validators.length(min=30)])


#User register
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        token = form.token.data
        #Create cursor
        cur = mysql.connection.cursor()
        #Execute query
        cur.execute("INSERT INTO users(name, email, username, password, token) VALUES(%s, %s, %s, %s, %s)",(name, email, username, password, token))
        #Commit ot db
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('You are now registered and can log in','success')
        return redirect(url_for('login'))
        #return 'ok'
    return render_template('register.html', form=form)

#User Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Get Form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #Create a Cursor
        cur = mysql.connection.cursor()

        #Get user by Username
        result = cur.execute("SELECT * FROM users WHERE username=%s",[username])

        if result >0 :
            #Get stored hash
            data = cur. fetchone()
            password = data['password']

            #Compare Passwords
            if sha256_crypt.verify(password_candidate,password):
                #app.logger.info('PASSWORD MATCHED')
                #Passed
                session['logged_in']= True
                session['username'] = username
                flash('You are now logged in','success')
                return redirect(url_for('dashbord'))
            else:
                error='Invalid login'
                return render_template('login.html',error=error)
            #Closed connection
            cur.close()
        else:
            error='Username not found'
            return render_template('login.html',error=error)


        #cur.close()

    return render_template('login.html')



#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#Dashbord
@app.route('/dashbord')
@is_logged_in
def dashbord():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('dashbord.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashbord.html', msg=msg)
    # Close connection
    cur.close()

#Add_articles
@app.route('/add_article', methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method =='POST' and form.validate():
        title = form.title.data
        body = form.body.data
        #Create cursor
        cur = mysql.connection.cursor()
        #Execute query
        cur.execute("INSERT INTO articles(title,author,body) VALUES(%s,%s,%s)",(title,session['username'],body))
        #Commit ot db
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('You are now added a new one article','success')
        return redirect(url_for('dashbord'))
    return render_template('add_article.html',form=form)



@app.route('/webhook/',methods=['POST','GET'])
def webhook():
    if request.method=='POST':
        r = request.get_json()
        write_json(r)
        chat_id=r['message']['chat']['id']
        text=r['message']['text']
        write_json(text)
        pattern =r'/\w+'
        if re.search(pattern,text):
            price = get_price(parc_text(text))
            send_message(chat_id,price)

        global last_msg
        last_msg=json.dumps(r,ensure_ascii=False)

        return jsonify(r)
    return '<h1>Hello bot</h1>'

@app.route('/last_msg/',methods=['POST','GET'])
@auth.login_required
#curl -u vorovik:python123 -i https://vorovik.pythonanywhere.com/last_msg/
def tes():
    r='<h2>{}</h2>'.format(last_msg)
    return r

def main():
    global kk
    if kk==1:
        for number in range(150):
            base[1].shema=str(number)
    kk=0
    pass

'''
'''
@app.route('/123')
def index123():
    return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
'''
'''

if __name__ =='__main__':
    socketio.run(app, host='0.0.0.0',port=5000, debug=True)
    main()
    #app.run('0.0.0.0',port=5000)
