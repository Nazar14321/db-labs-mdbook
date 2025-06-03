from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import CHAR, INTEGER, TEXT, TIMESTAMP

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'  # Якщо у вас назва таблиці була саме з великої літери

    id        = db.Column(CHAR(36), primary_key=True, default=db.func.UUID())  # MySQL 8.0+ дозволяє DB_FUNC.UUID()
    nickname  = db.Column(TEXT, nullable=False, unique=True)
    email     = db.Column(TEXT, nullable=False, unique=True)
    password  = db.Column(TEXT, nullable=False)
    photo     = db.Column(TEXT, nullable=True)




class Project(db.Model):
    __tablename__ = 'Project'

    id   = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(TEXT, nullable=False)


class Team(db.Model):
    __tablename__ = 'Team'

    id         = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name       = db.Column(TEXT, nullable=False)
    project_id = db.Column(INTEGER, db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


class Role(db.Model):
    __tablename__ = 'Role'

    id          = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name        = db.Column(TEXT, nullable=False)
    description = db.Column(TEXT, nullable=True)
    project_id  = db.Column(INTEGER, db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


class UserProject(db.Model):
    __tablename__ = 'User_Project'

    id         = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id    = db.Column(CHAR(36), db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    project_id = db.Column(INTEGER, db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    role_id    = db.Column(INTEGER, db.ForeignKey('Role.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    team_id    = db.Column(INTEGER, db.ForeignKey('Team.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)


class Task(db.Model):
    __tablename__ = 'Task'

    id           = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name         = db.Column(TEXT, nullable=False)
    description  = db.Column(TEXT, nullable=True)
    startDate    = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    deadlineDate = db.Column(TIMESTAMP, nullable=True)
    team_id      = db.Column(INTEGER, db.ForeignKey('Team.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)




class Artifact(db.Model):
    __tablename__ = 'Artifact'

    id       = db.Column(INTEGER, primary_key=True, autoincrement=True)
    status   = db.Column(TEXT, nullable=False)
    comment  = db.Column(TEXT, nullable=True)
    datetime = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    task_id  = db.Column(INTEGER, db.ForeignKey('Task.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


class Action(db.Model):
    __tablename__ = 'Action'

    id     = db.Column(INTEGER, primary_key=True, autoincrement=True)
    action = db.Column(TEXT, unique=True, nullable=False)


class RoleAction(db.Model):
    __tablename__ = 'Role_Action'

    id        = db.Column(INTEGER, primary_key=True, autoincrement=True)
    role_id   = db.Column(INTEGER, db.ForeignKey('Role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    action_id = db.Column(INTEGER, db.ForeignKey('Action.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


class Event(db.Model):
    __tablename__ = 'Event'

    id       = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id  = db.Column(CHAR(36), db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    role_id  = db.Column(INTEGER, db.ForeignKey('Role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    action   = db.Column(TEXT, nullable=False)
    datetime = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
