from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'your secret key'
app.debug = True


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/homepage')
def homepage():
    return render_template('home.html')
    
@app.route('/indexprof')
def indexprof():
    return render_template('indexProf.html')
    
@app.route('/indexstud')
def indexstud():
    return render_template('index.html')

# This code implements a Flask application with multiple routes for user login and logout.

# Route for student login. It will receive a POST request from the login form, 
# extract the username and password, and validate the credentials against the 
# 'Students' table in a SQLite database. If the credentials are valid, it will 
# store the user information in session variables and redirect the user to the 
# index page. If the credentials are invalid, it will display an error message.
@app.route('/loginStudent', methods=['GET', 'POST'])
def loginStudent():
    # Message to be displayed on the login page
    msg = ''
    # Check if the request is a POST request and the form has the required fields
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Extract the form data
        username = request.form['username']
        password = request.form['password']
        # Connect to the database
        conn = sqlite3.connect('database.db')
        # Create a cursor object
        curs = conn.cursor()
        # Execute a query to retrieve the user information based on the provided email and password
        curs.execute('SELECT * FROM Students WHERE email = ? AND password = ?', (username, password,))
        account = curs.fetchone()
        # Close the database connection
        conn.close()
        # If the user information is retrieved, store the information in session variables
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    # Render the login form template with the error message (if any)
    return render_template('loginStud.html', msg=msg)

# Route for professor login. It functions similarly to the student login route, but validates 
# the credentials against the 'Professors' table in the database.
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

# Route for the professor index page. It retrieves the username from the session variables 
# and passes it to the index template.
@app.route('/indexProf')
def indexProf():
    msg=session['username']
    return render_template('indexProf.html',msg=msg)


# this function logs out the user by popping out the values stored in session for 'loggedin', 'id', and 'username'
@app.route('/logout')
def logout():
    # "pop" function removes the specified key and value from the session
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # redirects the user back to the home page
    return redirect(url_for('home'))

#this function creates a new post and inserts it into the posts table in the database.it can be accessed through the create_post.html template.

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        # if the request method is POST, the function retrieves the values of "title", "description", "count" from the form.
        title = request.form['title']
        description = request.form['description']
        date_posted = datetime.datetime.now()
        count = request.form['count']
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        # inserts the values into the posts table in the database
        curs.execute('INSERT INTO posts (title, description,professor_id,date_posted,max_count,curr_count) VALUES (?, ?, ?, ?, ?, ?)', (title, description,session['id'],date_posted,count,0))
        conn.commit()
        conn.close()
        # redirects the user to the jobsPosted page, with the professor_id stored in the session as a parameter
        return redirect(url_for('jobsPosted',prof_id=session['id']))
    # if the request method is GET, the create_post.html template is returned, with the "msg" variable set to the username stored in the session.
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
    #check if the student has already been approved for a post
    cursor.execute("SELECT COUNT(*) FROM applications WHERE student_id = ? AND status='approved' ", (student_id,))
    st=cursor.fetchone()[0]

    if st > 0:
        message = "You have already been approved for a post."
        conn.close()
        return render_template('posts.html', message=message,posts=posts)

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
    # Connect to the database
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # Get all the posts from the database
    curs.execute('SELECT * FROM posts')
    posts = curs.fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)
    
@app.route('/<prof_id>/p')
def prof_profile(prof_id):   
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # Get the details of the professor with the specified id
    curs.execute('SELECT * FROM Professors where id = ?',(prof_id,))
    prof = curs.fetchone()
    conn.close()
    return render_template('profileProf.html', prof=prof)


@app.route('/<student_id>/s')
def stud_profile(student_id):   
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # Get the details of the student with the specified id
    curs.execute('SELECT * FROM Students where id = ?',(student_id,))
    stud = curs.fetchone()
    conn.close()
    return render_template('profileStud.html', stud=stud)

#view professor's profile by student
@app.route('/<prof_id>/profprofstud')
def profprofstud(prof_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # Get the details of the professor with the specified id
    curs.execute('SELECT * FROM Professors where id = ?',(prof_id,))
    prof = curs.fetchone()
    conn.close()
    return render_template('profprofstud.html', prof=prof)

#view student's profile by professor
@app.route('/<student_id>/studprofprof')
def studprofprof(student_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # Get the details of the student with the specified id
    curs.execute('SELECT * FROM Students where id = ?',(student_id,))
    stud = curs.fetchone()
    conn.close()
    return render_template('studprofprof.html', stud=stud)

# all jobs posted by professor
@app.route('/jobsPosted/<prof_id>')
def jobsPosted(prof_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # get all the posts from the database where the professor_id is the same as the id of the professor who is logged in
    curs.execute('SELECT * FROM posts where professor_id=?',(prof_id,))
    posts = curs.fetchall()
    conn.close()
    return render_template('profPosts.html', posts=posts)

#delete post by professor
@app.route('/<int:id>/<prof_id>/delete')
def delete(id,prof_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # delete the post with the specified id
    curs.execute('DELETE FROM posts WHERE id = ?', (id,))
    # get all the posts from the database where the professor_id is the same as the id of the professor who is logged in
    curs.execute('SELECT * FROM posts where professor_id=?', (prof_id,))
    posts = curs.fetchall()
    # delete all the applications for the post with the specified id
    curs.execute('DELETE FROM applications WHERE post_id = ?', (id,))
    conn.commit()
    conn.close()
    message = "Your job has been deleted."
    return render_template('profPosts.html', posts=posts,message=message)

#view applications for that post
@app.route('/<int:id>/view_applications')
def view_applications(id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # get all the applications for the post with the specified id with the related attributes
    curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(id,))
    applications = curs.fetchall()
    # get the title of the post with the specified id
    curs.execute('SELECT title FROM posts where id=?',(id,))
    postname = curs.fetchone()
    conn.close()
    return render_template('view_applications.html', applications=applications,postname=postname)

#view applications for that student
@app.route('/<int:id>/view_applications_student')
def view_applications_student(id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()    
    # get all the applications for the student with the specified id with the related attributes
    curs.execute('SELECT posts.title, posts.description, professors.id, applications.status FROM posts, applications, professors WHERE posts.id = applications.post_id AND professors.id = posts.professor_id AND applications.student_id = ?;',(id,))
    applications = curs.fetchall()
    conn.close()
    return render_template('view_applications_student.html', applications=applications)

#edit profile for the student
@app.route('/<int:id>/edit_student', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # get the details of the student with the specified id
    curs.execute('SELECT * FROM Students where id = ?',(id,))
    stud = curs.fetchone()
    conn.close()
    if request.method == 'POST':
        about = request.form['about']
        conn = sqlite3.connect('database.db')
        curs = conn.cursor()
        # update the details of the student with the specified id
        curs.execute('UPDATE Students SET about = ? WHERE id = ?', (about, id))
        conn.commit()
        conn.close()
        message = "Your profile has been updated."
        return redirect(url_for('stud_profile',student_id=id))
    return render_template('edit_student.html', stud=stud)

#approve application for that post and student
@app.route('/<int:application_id>/<int:post_id>/<int:student_id>/approve')
def approve(application_id,student_id,post_id):

    conn = sqlite3.connect('database.db')
    curs = conn.cursor()

    #check if post is still available
    curs.execute('SELECT max_count,curr_count FROM posts WHERE id = ?', (post_id,))
    counts = curs.fetchone()
    #if post is full, display message Max number of applications approved
    if counts[1] == counts[0]:
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Maximum number of applications approved."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)


    #fetch the status of the application
    curs.execute('SELECT status FROM applications WHERE id = ?', (application_id,))
    status = curs.fetchone()

    #if application is unavailable, display message Application unavailable
    if status[0] == "unavailable":
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Application unavailable."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)

    #if application is already rejected, display message Application already rejected
    if status[0] == "rejected":
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Application already rejected."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)

    #if application is already approved, display message Application already approved
    if status[0] == "approved":
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Application already approved."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)


    #if application is pending, approve it
    curs.execute('UPDATE applications SET status = "approved" WHERE id = ?', (application_id,))
    #update the current count of the post
    curs.execute('UPDATE posts SET curr_count = curr_count + 1 WHERE id = ?', (post_id,))
    #update the status of all other pending applications for the post to unavailable
    curs.execute('UPDATE applications SET status = "unavailable" WHERE student_id = ? AND NOT (id=?)', (student_id,application_id,))
    
    curs.execute('SELECT max_count,curr_count FROM posts WHERE id = ?', (post_id,))
    counts = curs.fetchone()
    #if post is full, update the status of all pending applications for the post to closed
    if counts[1] == counts[0]:
        curs.execute('UPDATE applications SET status = "closed" WHERE post_id = ? and status ="pending" ', (post_id,))
        
    #get all the applications for the post with the related attributes
    curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
    applications = curs.fetchall()
    curs.execute('SELECT title FROM posts where id=?',(post_id,))
    postname = curs.fetchone()
    conn.commit()
    conn.close()
    message = "Application approved."
    return render_template('view_applications.html', applications=applications,message=message,postname=postname)

#reject application for that post and student
@app.route('/<int:application_id>/<int:post_id>/<int:student_id>/reject')
def reject(application_id,post_id,student_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    # if approved, cannot be rejected
    curs.execute('SELECT status FROM applications WHERE id = ?', (application_id,))
    status = curs.fetchone()
    if status[0] == "approved":
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Application already approved."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)
    #if unavailable, cannot be rejected
    if status[0] == "unavailable":
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Application unavailable."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)
    #if closed, cannot be rejected
    if status[0] == "closed":
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Application closed."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)
    #if rejected, cannot be rejected
    if status[0] == "rejected":
        curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
        applications = curs.fetchall()
        curs.execute('SELECT title FROM posts where id=?',(post_id,))
        postname = curs.fetchone()
        conn.commit()
        conn.close()
        message = "Application already rejected."
        return render_template('view_applications.html', applications=applications,message=message,postname=postname)

    #if pending, reject it
    curs.execute('UPDATE applications SET status = "rejected" WHERE id = ?', (application_id,))
    #get all the applications for the post with the related attributes
    curs.execute('SELECT Applications.id as applicationID,post_id,student_id,name,email,status FROM applications,Students where post_id=? AND applications.student_id=Students.id;',(post_id,))
    applications = curs.fetchall()
    curs.execute('SELECT title FROM posts where id=?',(post_id,))
    postname = curs.fetchone()
    conn.commit()
    conn.close()
    message = "Application rejected."
    return render_template('view_applications.html', applications=applications,message=message,postname=postname)
