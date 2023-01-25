from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'your secret key'
app.debug = True


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/loginStudent', methods=['GET', 'POST'])
def loginStudent():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM Students WHERE email = ? AND password = ?', (username, password,))
        account = curs.fetchone()
        conn.close()
        if account:
       
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('loginStud.html', msg=msg)


@app.route('/loginProf', methods=['GET', 'POST'])
def loginProf():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM Professors WHERE email = ? AND password = ?', (username, password,))
        account = curs.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('indexProf.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('loginProf.html', msg=msg)

@app.route('/indexProf')
def indexProf():
    msg=session['username']
    return render_template('indexProf.html',msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_posted = datetime.datetime.now()
        count = request.form['count']
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        curs.execute('INSERT INTO posts (title, description,professor_id,date_posted,max_count,curr_count) VALUES (?, ?, ?, ?, ?, ?)', (title, description,session['id'],date_posted,count,0))
        conn.commit()
        conn.close()
        return redirect(url_for('indexProf'))
    msg=session['username']
    return render_template('create_post.html',msg=msg)



@app.route("/apply/<post_id>")
def apply(post_id):
    # Connect to the database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    # Get the post_id, student_id and date_applied from the request
    student_id = session["id"]


    # Check if the student has already applied for the post
    cursor.execute("SELECT COUNT(*) FROM applications WHERE post_id = ? AND student_id = ?", (post_id, student_id))
    count = cursor.fetchone()[0]

    if count > 0:
        # The student has already applied for the post
        message = "You have already applied for this post."
    else:
        # Insert the new application into the "applications" table
        cursor.execute("INSERT INTO applications (post_id, student_id) VALUES (?, ?)", (post_id, student_id))
        conn.commit()
        message = "Your application has been received."

    # Close the connection
    conn.close()

    return render_template('posts.html', message=message,posts=posts)

#create function to get all posts
@app.route('/posts')
def posts():
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM posts')
    posts = curs.fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)
    
@app.route('/<prof_id>/p')
def prof_profile(prof_id):   
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM Professors where id = ?',(prof_id,))
    prof = curs.fetchone()
    conn.close()
    return render_template('profileProf.html', prof=prof)


@app.route('/<student_id>/s')
def stud_profile(student_id):   
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM Students where id = ?',(student_id,))
    stud = curs.fetchone()
    conn.close()
    return render_template('profileStud.html', stud=stud)

@app.route('/jobsPosted/<prof_id>')
def jobsPosted(prof_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM posts where professor_id=?',(prof_id,))
    posts = curs.fetchall()
    conn.close()
    return render_template('profPosts.html', posts=posts)

@app.route('/<int:id>/<prof_id>/delete')
def delete(id,prof_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute('DELETE FROM posts WHERE id = ?', (id,))
    curs.execute('SELECT * FROM posts where professor_id=?', (prof_id,))
    posts = curs.fetchall()
    conn.commit()
    conn.close()
    message = "Your job has been deleted."
    return render_template('profPosts.html', posts=posts,message=message)
