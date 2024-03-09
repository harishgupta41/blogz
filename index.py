from flask import Flask, render_template, request, redirect, make_response, Response
import mysql.connector
# import argon2
import uuid

mydb = mysql.connector.connect(
    host="localhost",
    database="harry",
    username="harry",
    password="dl3san3581"
)
cursor = mydb.cursor()

app=Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    if request.cookies.get('user'):
        print(request.cookies.get('user'))
    else:
        print("cookie not set")
    cursor.execute('select * from posts limit 10');
    data=cursor.fetchall()
    # print(data)
    # print(type(data[1]))
    return render_template('home.html',title="home",data=data)

@app.route('/view')
def view():
    postid = request.args.get('id')
    cursor.execute('select * from posts where post_id="{0}"'.format(postid))
    data=cursor.fetchall()
    # print(data)
    return render_template('view.html',title=data[0][3],data=data[0])
    
@app.route('/login')
def login():
    return render_template('login.html',title="login")

@app.route('/user_login', methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        username = request.form['user']
        passwd = request.form['pswd']
        cursor.execute("SELECT * FROM users WHERE user_name='{0}' AND password=md5('{1}')".format(username, passwd))
        data = cursor.fetchall()
        if(data):
            resp=make_response(redirect('/'))
            resp.set_cookie('user',username)
            return resp
        else:
            return redirect('/login')
        
@app.route('/registration')
def registration():
    return render_template('register.html',title="registration")

@app.route('/user_register',methods=["POST"])
def user_register():
    if request.method == "POST":
        fname=request.form['fname']
        lname=request.form['lname']
        gmail=request.form['gmail']
        uname = request.form['uname']
        password=request.form['passwd']
        repassword=request.form['repasswd']
        if (password!=repassword):
            return redirect('/registration')
        else:
            cursor.execute("insert into users(user_name, fname, lname, gmail, password) values('{0}', '{1}', '{2}', '{3}', md5('{4}'))".format(uname, fname, lname, gmail, password))
            mydb.commit()
            return redirect('/login')
        # print(fname,lname,gmail,password,repassword)

@app.route('/new-blog')
def new_blog():
    if "user" not in request.cookies:
        return render_template('access.html',title="access-denied")
    return render_template('new.html',title="new-blog")

@app.route('/posting',methods=["POST"])
def posting():
    if request.method == "POST":
        title=request.form['title']
        post=request.form['blogpost']
        author=request.cookies.get('user')
        postid=uuid.uuid4().hex
        cursor.execute('insert into posts(post_id, author, title, post_body) values("{0}", "{1}", "{2}","{3}")'.format(postid,author,title,post))
        mydb.commit()
        return redirect('/')
    
@app.route('/myprofile')
def myprofile():
    if "user" not in request.cookies:
        return render_template('access.html',title="access-denied")
    cursor.execute('select * from users where user_name="{0}"'.format(request.cookies.get('user')))
    data=cursor.fetchall()
    return render_template('profile.html',title="my-profile",data=data[0])

@app.route('/myblogs')
def myblogs():
    if "user" not in request.cookies:
        return render_template('access.html',title="access-denied")
    cursor.execute('select * from posts where author="{0}"'.format(request.cookies.get('user')))
    data=cursor.fetchall()
    return render_template('home.html',title="my-blogs",data=data)

@app.route('/logout')
def logout():
    response = make_response(render_template('logout.html',title='logging-out'))
    response.set_cookie('user', '', max_age=0)
    return response

if __name__=="__main__":
    app.run(debug=True)