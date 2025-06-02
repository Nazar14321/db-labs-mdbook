from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import CHAR, INTEGER, TEXT, TIMESTAMP

db = SQLAlchemy()

# ------------------------------------------------------------
# 1. Клас User
# ------------------------------------------------------------
class User(db.Model):
    __tablename__ = 'User'  # Якщо у вас назва таблиці була саме з великої літери

    id        = db.Column(CHAR(36), primary_key=True, default=db.func.UUID())  # MySQL 8.0+ дозволяє DB_FUNC.UUID()
    nickname  = db.Column(TEXT, nullable=False, unique=True)
    email     = db.Column(TEXT, nullable=False, unique=True)
    password  = db.Column(TEXT, nullable=False)
    photo     = db.Column(TEXT, nullable=True)

    # Наприклад, можна додати зв’язки (relationship) з іншими моделями:
    # projects = db.relationship('UserProject', backref='user', lazy='dynamic')


# ------------------------------------------------------------
# 2. Клас Project
# ------------------------------------------------------------
class Project(db.Model):
    __tablename__ = 'Project'

    id   = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(TEXT, nullable=False)

    # teams = db.relationship('Team', backref='project', lazy='dynamic')
    # roles = db.relationship('Role', backref='project', lazy='dynamic')
    # user_projects = db.relationship('UserProject', backref='project', lazy='dynamic')


# ------------------------------------------------------------
# 3. Клас Team
# ------------------------------------------------------------
class Team(db.Model):
    __tablename__ = 'Team'

    id         = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name       = db.Column(TEXT, nullable=False)
    project_id = db.Column(INTEGER, db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    # tasks = db.relationship('Task', backref='team', lazy='dynamic')


# ------------------------------------------------------------
# 4. Клас Role
# ------------------------------------------------------------
class Role(db.Model):
    __tablename__ = 'Role'

    id          = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name        = db.Column(TEXT, nullable=False)
    description = db.Column(TEXT, nullable=True)
    project_id  = db.Column(INTEGER, db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    # role_actions = db.relationship('RoleAction', backref='role', lazy='dynamic')
    # user_projects = db.relationship('UserProject', backref='role', lazy='dynamic')


# ------------------------------------------------------------
# 5. Клас UserProject (зв’язок користувачів з проєктами)
# ------------------------------------------------------------
class UserProject(db.Model):
    __tablename__ = 'User_Project'

    id         = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id    = db.Column(CHAR(36), db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    project_id = db.Column(INTEGER, db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    role_id    = db.Column(INTEGER, db.ForeignKey('Role.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    team_id    = db.Column(INTEGER, db.ForeignKey('Team.id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)


# ------------------------------------------------------------
# 6. Клас Task
# ------------------------------------------------------------
class Task(db.Model):
    __tablename__ = 'Task'

    id           = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name         = db.Column(TEXT, nullable=False)
    description  = db.Column(TEXT, nullable=True)
    startDate    = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    deadlineDate = db.Column(TIMESTAMP, nullable=True)
    team_id      = db.Column(INTEGER, db.ForeignKey('Team.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    # artifacts = db.relationship('Artifact', backref='task', lazy='dynamic')


# ------------------------------------------------------------
# 7. Клас Artifact
# ------------------------------------------------------------
class Artifact(db.Model):
    __tablename__ = 'Artifact'

    id       = db.Column(INTEGER, primary_key=True, autoincrement=True)
    status   = db.Column(TEXT, nullable=False)
    comment  = db.Column(TEXT, nullable=True)
    datetime = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    task_id  = db.Column(INTEGER, db.ForeignKey('Task.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


# ------------------------------------------------------------
# 8. Клас Action
# ------------------------------------------------------------
class Action(db.Model):
    __tablename__ = 'Action'

    id     = db.Column(INTEGER, primary_key=True, autoincrement=True)
    action = db.Column(TEXT, unique=True, nullable=False)

    # role_actions = db.relationship('RoleAction', backref='action', lazy='dynamic')


# ------------------------------------------------------------
# 9. Клас RoleAction
# ------------------------------------------------------------
class RoleAction(db.Model):
    __tablename__ = 'Role_Action'

    id        = db.Column(INTEGER, primary_key=True, autoincrement=True)
    role_id   = db.Column(INTEGER, db.ForeignKey('Role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    action_id = db.Column(INTEGER, db.ForeignKey('Action.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


# ------------------------------------------------------------
# 10. Клас Event
# ------------------------------------------------------------
class Event(db.Model):
    __tablename__ = 'Event'

    id       = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id  = db.Column(CHAR(36), db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    role_id  = db.Column(INTEGER, db.ForeignKey('Role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    action   = db.Column(TEXT, nullable=False)
    datetime = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
