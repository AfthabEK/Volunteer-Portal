# Volunteer Portal

This is a web-based volunteer management system that connects students and professors for volunteer opportunities.The website is currently hosted [here](http://afthabek.pythonanywhere.com/).

## Technologies Used

 - Flask
 - Jinja2
 - Sqlite3
 - HTML
 - CSS
 - JavaScript

## Features

- Professors can log in and create volunteer posts, edit and delete them, approve or reject student applications, view the profiles of applicants, and set the required number of volunteers for each post.
- Students can log in and view available volunteer posts, apply for them and see their application status.
- Application status is updated in real-time, with student profiles and professor details stored in the database.
 
- Students can apply to multiple posts, but can only be accepted for one. Approved applications cause the rest of the student's applications to be marked as unavailable and the maximum number of approved students cause the post to be marked as closed.
- Professors and professors can view each others' profiles contact each other via email.
- Students can view their own profile and edit it.

## Sample Login Credentials
- Professor email: professor@nitc.ac.in
	password: password

- Student email: student@gmail.com
	password: password

## Running the Project Locally

Clone the repository to your local machine and install the necessary dependencies.
    
    ```bash
    git clone https://github.com/AfthabEK/volunteer-portal.git
    cd volunteer-portal
    pip install -r requirements.txt
    ```
Run the application.
    
    ```bash
    python app.py
    ```
The project will be available at localhost:5000.

## Contributions
Contributions are always welcome! Feel free to submit a pull request.







