from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Helper functions
##############################################################################
# Model definitions

class User(db.Model):
    """User of calendar website."""

    __tablename__ = "users"

    user_id = user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return(f"<User user_id={self.user_id} email={self.email}>")


class Event(db.Model):

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    venue = db.Column(db.String, nullable=True)

    def __repr__(self):
        return(f"<event id={self.event_id} name={self.event_name}>")  

           


class Guest(db.Model):
# association table
    __tablename__= "guests"

    guest_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable = False)

    user = db.relationship("User", backref=db.backref("guests", order_by=guest_id))

    event = db.relationship("Event", backref=db.backref("guests", order_by=guest_id))


    def __repr__(self):
        return(f"""<Guest guest_id={self.guest_id} event_id={self.event_id},
             user_id={self.user_id})""")


class Task(db.Model):
    __tablename__="tasks"

    task_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False) 
    created_on = db.Column(db.DateTime, nullable=True)  
    complete_by = db.Column(db.DateTime, nullable=True)

    def __repr__(self): 
        return(f""" <Task task_id={self.task_id} user_id{self.user_id} created_on={self.created_on} complete_by={self.complete_by}""")   


class Project(db.Model):

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)
    complete_by = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return(f"<project project_id={self.project_id} project_name={self.project_name}>")                         

class ProjectMember(db.Model):

    # association table

    __tablename__= "projects_members"

    project_member_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable = False)

    user = db.relationship("User", backref=db.backref("projects_members", order_by=project_member_id))

    project = db.relationship("ProjectMember", backref=db.backref("projects_members", order_by=project_member_id))


    def __repr__(self):
        return(f"""<ProjectMember project_member_id={self.project_member_id} project_id={self.project_id},
             user_id={self.user_id})""")

##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///calendar'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")