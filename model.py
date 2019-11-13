from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_jwt_extended import JWTManager
from passlib.hash import pbkdf2_sha256 as sha256
from flask_cors import CORS

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


db = SQLAlchemy()
jwt = JWTManager()
app = Flask(__name__)
CORS(app)
api = Api(app)


# db = SQLAlchemy()

##############################################################################
# Helper functions
##############################################################################
# Model definitions



class User(db.Model):
    """User of calendar website."""

    __tablename__ = "users"

    user_id = user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(120), nullable=True)

    projects = db.relationship('Project', secondary = 'projects_members')

    # projects = db.relationship("ProjectMember", back_populates="users")
    # projects = db.relationship("project", 
    #                             secondary=association_table,
    #                             back_populates="users")

                           


                            



    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)  

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()      

    def __repr__(self):
        return(f"<User user_id={self.user_id} email={self.email}>")

class Project(db.Model):

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    admin_id = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)
    complete_by = db.Column(db.DateTime, nullable=True)

    users = db.relationship('User', secondary = 'projects_members')

    # users = db.relationship("User", back_populates="Project")

    # users = db.relationship("user",
    #                         secondary=association_table,
    #                         back_populates="projects") 
    

    def __repr__(self):
        return(f"<project project_id={self.project_id} project_name={self.project_name}>")                         


class ProjectMember(db.Model):
    __tablename__="projects_members"


    project_id = db.Column(
    db.Integer, 
    ForeignKey('projects.project_id'), 
    primary_key = True)
    user_id = db.Column(
    db.Integer, 
    ForeignKey('users.user_id'), 
    primary_key = True)  
  

        


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)   

# @app.before_first_request
# def create_tables():
#     db.create_all()

# app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# jwt = JWTManager(app)


# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return RevokedTokenModel.is_jti_blacklisted(jti)             


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
    task_name =  db.Column(db.String(100), nullable=False) 
    task_description =  db.Column(db.String(300), nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)  
    complete_by = db.Column(db.DateTime, nullable=True)

    def __repr__(self): 
        return(f""" <Task task_id={self.task_id} user_id{self.user_id} created_on={self.created_on} complete_by={self.complete_by}""")   


# class Project(db.Model):

#     __tablename__ = "projects"

#     project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     project_name = db.Column(db.String, nullable=False)
#     admin_id = db.Column(db.String, nullable=True)
#     description = db.Column(db.String, nullable=True)
#     created_on = db.Column(db.DateTime, nullable=True)
#     complete_by = db.Column(db.DateTime, nullable=True)

#     # users = db.relationship("User", back_populates="Project")

#     users = db.relationship("user",
#                             secondary=association_table,
#                             back_populates="projects") 
    

#     def __repr__(self):
#         return(f"<project project_id={self.project_id} project_name={self.project_name}>")                         


# association_table = db.Table('association', Base.metadata,
#     db.Column('user_id', db.Integer, ForeignKey('user.id')),
#     db.Column('project_id', db.Integer, ForeignKey('project.id'))
# ) 
# class ProjectMember(db.Model):

#     # association table

#     __tablename__= "projects_members"

#     # project_member_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
#     # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
#     # project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable = False)
#     # user = db.relationship("User", backref=db.backref("projects_members", order_by=project_member_id))

#     # project = db.relationship("Project", backref=db.backref("projects_members", order_by=project_member_id))

#     user_id = db.Column(db.Integer, ForeignKey('user.user_id'), primary_key=True)
#     project_id = db.Column(db.Integer, ForeignKey('project.project_id'), primary_key=True)
    
#     project  = db.relationship("Project", back_populates='users')
#     user = db.relationship("User", back_populates='projects')

#     def __repr__(self):
#         return(f"""<ProjectMember project_member_id={self.project_member_id} project_id={self.project_id},
#              user_id={self.user_id})""")

##############################################################################
# Helper functions
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///calendar'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    # jwt = JWTManager(app)


    # app.config['JWT_BLACKLIST_ENABLED'] = True
    # app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    db.app = app
    db.init_app(app)
    jwt.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all()
    

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# jwt = JWTManager(app)


app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


# import server

# api.add_resource(server.UserRegistration, '/registration')
# api.add_resource(server.UserLogin, '/login')
# api.add_resource(server.signin, '/signin')


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")