from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, make_response, flash)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Event, Guest, Task, Project, connect_to_db, db, RevokedTokenModel)

import jsonify

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from datetime import datetime

app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

# class UserLogin(Server):
#     def post(self):
#         return {'message': 'User login'}
      


@app.route('/')
def index():
    """Index page"""
    return render_template("index.html")
   
  


@app.route('/registration-form')
def register():
    """Registeration page"""
    return render_template('registration_form.html')


@app.route('/sign-up', methods=["POST"])
def sign_up():
    """Check if user email exists in database and add them as new user if not"""

    email = request.form['email']
    password = request.form['password']
    match = User.query.filter_by(email=email).all()  

    if not match:
        new_user = User(email=email, password=User.generate_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return render_template("registration-submitted.html", status="added",
            email=email)
       

    else:
        return render_template("registration-submitted.html", status="preexisting", 
            email=email)


@app.route('/login')
def login():
    """login page"""
    return render_template('login.html')    

@app.route('/signin', methods=['POST'])
def signin():
    """ sign in form"""

    email = request.form['email']
    password = request.form['password']

    current_user = User.find_by_email(email)

    if not current_user:
        return jsonify({'message': 'User {} doesn\'t exist'.format(email)})

    if User.verify_hash(password, current_user.password):
            
            access_token = create_access_token(identity = email)
            refresh_token = create_refresh_token(identity = email)


            # response.header = {"Content-Type: text/turtle", "Content-Location: mydata.ttl"
            #  "Access-Control-Allow-Origin: *"}
           
            resp = make_response(render_template('homepage.html'))
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)


             #insert flash to let the user know they are logged in 

            return resp
    else:

        flash("The username and password you entered do not match. Please try again")
        return redirect('/login')


@app.route('/logout', methods=["POST"])
@jwt_required
def logout():

    jti =get_raw_jwt()['jti']
    print(get_raw_jwt()['jti'])

    try:
        revoked_token = RevokedTokenModel(jti = jti)
        revoked_token.add()
        resp = {'message': 'Refresh token has been revoked'}
        unset_jwt_cookies(resp)
        return resp
    except:
        return {'message': 'Something went wrong'}, 500





       


@app.route('/test')
@jwt_required
def test():
    #get current user
    current_user= get_jwt_identity()
    people = db.session.query(User.email, Task.task_name, Task.task_description).join(Task).all()
    for email, task_name, task_description in people:
        if email == current_user:
            print(email, task_name, task_description)
    return {'hello':'world'}
                          
@app.route('/tasks')  
@jwt_required
def tasks():
    current_user = get_jwt_identity()

    # user = User.query.filter_by(email=current_user).one()
    # user_id = user.user_id
    # print("============", user_id)
    # tasks = Task.query.filter_by(user_id = user_id).all()

    #refactored: only making 1 query to db instead of 2
    all_tasks = db.session.query(User.email, Task.task_id, Task.task_name, Task.task_description).join(Task).all()

    tasks = []
    for item in all_tasks:
        if item.email == current_user:
            tasks.append(item)


    return render_template("tasks.html", tasks = tasks)


# @app.route('/addtaskform') 
# @jwt_required
# def add_task_form():
#     return render_template("add-task-form.html")   

@app.route('/addtask',methods=["POST"])
@jwt_required
def add_task():
    try:
        current_user = get_jwt_identity()
        print(current_user)
        user = User.find_by_email(current_user)
        #  print(user.user_id)
    # user = User.query.filter_by(email=current_user).all()
        user_id = user.user_id
        task_name = request.form['task']
        task_description = request.form['description']

        print( task_name, task_description)
        new_task = Task(user_id = user_id, task_name= task_name, task_description=task_description, created_on = datetime.now(), complete_by = datetime.now()) 
        db.session.add(new_task)
        db.session.commit()
        # tasks = Task.query.filter_by(user_id = user_id).all()

        return redirect("/tasks")

    except:
        return {'message': 'Something went wrong'}, 500 


@app.route('/deletetask/<task_id>') 
def delete_task(task_id):

    

    task = Task.query.filter_by(task_id =task_id).one()
    print("+++++++++========",task)
    db.session.delete(task)
    db.session.commit()


    return redirect('/tasks')

@app.route('/addproject') 
def addproject():
    return render_template('create_project.html')


@app.route('/project_add', methods=["POST"]) 
@jwt_required
def project_add():
    #get user id
    user = get_jwt_identity()
    current_user = User.find_by_email(user)
    user_id = current_user.user_id

    #create and add new project to projects table in db
    project_name = request.form['project_name']
    project_description = request.form['project_description']
    new_project = Project(project_name = project_name, description = project_description, admin_id=user_id)
    db.session.add(new_project)
    db.session.commit()

    # #get the project id for most recently added project 
    # current_project = Project.query.filter_by(project_name = project_name, description = project_description).first()
    # current_project_id = current_project.project_id

    # #add project id and user id to project_member table (association table)
    # new_project_member= ProjectMember(user_id=user_id, project_id = current_project_id)
    # db.session.add(new_project_member)
    # db.session.commit()

    return "added project "   




@app.route('/projects')
@jwt_required
def projects():
    user = get_jwt_identity()  
    print("USER", user)

    current_user = User.find_by_email(user)
    user_id = current_user.user_id
    projects_numbers = ProjectMember.query.filter_by(user_id = user_id).all()

    #projects_numbers = list of project numbers 
    projects=[]
    for project_id in projects_numbers:
       projects.append(Project.query.filter_by(project_id = project_id))
    print(projects)  

    # projects = Project.query.filter_by(project_id = project_id)



    return "projects"  

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')    