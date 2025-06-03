from flask import Flask, request, abort
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
api = Api(app)



from sqlalchemy.dialects.mysql import CHAR, INTEGER, TEXT, TIMESTAMP

class User(db.Model):
    __tablename__ = 'User'
    id         = db.Column(CHAR(36), primary_key=True, default=db.func.UUID())
    nickname   = db.Column(TEXT, nullable=False, unique=True)
    email      = db.Column(TEXT, nullable=False, unique=True)
    password   = db.Column(TEXT, nullable=False)
    photo      = db.Column(TEXT, nullable=True)
    team_id    = db.Column(
                    INTEGER,
                    db.ForeignKey('Team.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )


class Project(db.Model):
    __tablename__ = 'Project'
    id   = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(TEXT, nullable=False)


class Team(db.Model):
    __tablename__ = 'Team'
    id         = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name       = db.Column(TEXT, nullable=False)
    project_id = db.Column(
                    INTEGER,
                    db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )


class Role(db.Model):
    __tablename__ = 'Role'
    id          = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name        = db.Column(TEXT, nullable=False)
    description = db.Column(TEXT, nullable=True)
    project_id  = db.Column(
                    INTEGER,
                    db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )


class UserProject(db.Model):
    __tablename__ = 'User_Project'
    id         = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id    = db.Column(
                    CHAR(36),
                    db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )
    project_id = db.Column(
                    INTEGER,
                    db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )
    role_id    = db.Column(
                    INTEGER,
                    db.ForeignKey('Role.id', ondelete='SET NULL', onupdate='CASCADE'),
                    nullable=True
                 )
    team_id    = db.Column(
                    INTEGER,
                    db.ForeignKey('Team.id', ondelete='SET NULL', onupdate='CASCADE'),
                    nullable=True
                 )


class Task(db.Model):
    __tablename__ = 'Task'
    id           = db.Column(INTEGER, primary_key=True, autoincrement=True)
    name         = db.Column(TEXT, nullable=False)
    description  = db.Column(TEXT, nullable=True)
    startDate    = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    deadlineDate = db.Column(TIMESTAMP, nullable=True)
    team_id      = db.Column(
                     INTEGER,
                     db.ForeignKey('Team.id', ondelete='CASCADE', onupdate='CASCADE'),
                     nullable=False
                  )


class Artifact(db.Model):
    __tablename__ = 'Artifact'
    id       = db.Column(INTEGER, primary_key=True, autoincrement=True)
    status   = db.Column(TEXT, nullable=False)
    comment  = db.Column(TEXT, nullable=True)
    datetime = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    task_id  = db.Column(
                  INTEGER,
                  db.ForeignKey('Task.id', ondelete='CASCADE', onupdate='CASCADE'),
                  nullable=False
               )


class Action(db.Model):
    __tablename__ = 'Action'
    id     = db.Column(INTEGER, primary_key=True, autoincrement=True)
    action = db.Column(TEXT, unique=True, nullable=False)


class RoleAction(db.Model):
    __tablename__ = 'Role_Action'
    id        = db.Column(INTEGER, primary_key=True, autoincrement=True)
    role_id   = db.Column(
                    INTEGER,
                    db.ForeignKey('Role.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )
    action_id = db.Column(
                    INTEGER,
                    db.ForeignKey('Action.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )


class Event(db.Model):
    __tablename__ = 'Event'
    id       = db.Column(INTEGER, primary_key=True, autoincrement=True)
    user_id  = db.Column(
                    CHAR(36),
                    db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )
    role_id  = db.Column(
                    INTEGER,
                    db.ForeignKey('Role.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )
    action   = db.Column(TEXT, nullable=False)
    datetime = db.Column(TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


class ProjectListResource(Resource):
    def get(self):
        projects = Project.query.all()
        return [{"id": p.id, "name": p.name} for p in projects]

    def post(self):
        data = request.get_json(force=True)
        if "name" not in data or not data["name"].strip():
            abort(400, description="Field 'name' required")
        new = Project(name=data["name"].strip())
        db.session.add(new)
        db.session.commit()
        return {"id": new.id, "name": new.name}, 201


class ProjectResource(Resource):
    def get(self, project_id):
        proj = Project.query.get(project_id)
        if not proj:
            abort(404, description="Project not found")
        return {"id": proj.id, "name": proj.name}

    def put(self, project_id):
        proj = Project.query.get(project_id)
        if not proj:
            abort(404, description="Project not found")
        data = request.get_json(force=True)
        if "name" in data and data["name"].strip():
            proj.name = data["name"].strip()
        db.session.commit()
        return {"message": "Project updated"}

    def delete(self, project_id):
        proj = Project.query.get(project_id)
        if not proj:
            abort(404, description="Project not found")
        db.session.delete(proj)
        db.session.commit()
        return {"message": "Project deleted"}


class TeamListResource(Resource):
    def get(self):
        teams = Team.query.all()
        return [
            {"id": t.id, "name": t.name, "project_id": t.project_id}
            for t in teams
        ]

    def post(self):
        data = request.get_json(force=True)
        if "name" not in data or not data["name"].strip():
            abort(400, description="Field 'name' required")
        if "project_id" not in data:
            abort(400, description="Field 'project_id' required")

        if not Project.query.get(data["project_id"]):
            abort(404, description="Project not found")

        new = Team(name=data["name"].strip(), project_id=data["project_id"])
        db.session.add(new)
        db.session.commit()
        return {"id": new.id, "name": new.name, "project_id": new.project_id}, 201


class TeamResource(Resource):
    def get(self, team_id):
        t = Team.query.get(team_id)
        if not t:
            abort(404, description="Team not found")
        return {"id": t.id, "name": t.name, "project_id": t.project_id}

    def put(self, team_id):
        t = Team.query.get(team_id)
        if not t:
            abort(404, description="Team not found")
        data = request.get_json(force=True)
        if "name" in data and data["name"].strip():
            t.name = data["name"].strip()
        if "project_id" in data:
            if not Project.query.get(data["project_id"]):
                abort(404, description="Project not found")
            t.project_id = data["project_id"]
        db.session.commit()
        return {"message": "Team updated"}

    def delete(self, team_id):
        t = Team.query.get(team_id)
        if not t:
            abort(404, description="Team not found")
        db.session.delete(t)
        db.session.commit()
        return {"message": "Team deleted"}


class RoleListResource(Resource):
    def get(self):
        roles = Role.query.all()
        return [
            {"id": r.id, "name": r.name, "description": r.description, "project_id": r.project_id}
            for r in roles
        ]

    def post(self):
        data = request.get_json(force=True)
        if "name" not in data or not data["name"].strip():
            abort(400, description="Field 'name' required")
        if "project_id" not in data:
            abort(400, description="Field 'project_id' required")
        if not Project.query.get(data["project_id"]):
            abort(404, description="Project not found")

        new = Role(
            name=data["name"].strip(),
            description=data.get("description"),
            project_id=data["project_id"]
        )
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "name": new.name,
            "description": new.description,
            "project_id": new.project_id
        }, 201


class RoleResource(Resource):
    def get(self, role_id):
        r = Role.query.get(role_id)
        if not r:
            abort(404, description="Role not found")
        return {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "project_id": r.project_id
        }

    def put(self, role_id):
        r = Role.query.get(role_id)
        if not r:
            abort(404, description="Role not found")
        data = request.get_json(force=True)
        if "name" in data and data["name"].strip():
            r.name = data["name"].strip()
        if "description" in data:
            r.description = data["description"]
        if "project_id" in data:
            if not Project.query.get(data["project_id"]):
                abort(404, description="Project not found")
            r.project_id = data["project_id"]
        db.session.commit()
        return {"message": "Role updated"}

    def delete(self, role_id):
        r = Role.query.get(role_id)
        if not r:
            abort(404, description="Role not found")
        db.session.delete(r)
        db.session.commit()
        return {"message": "Role deleted"}


class UserProjectListResource(Resource):
    def get(self):
        ups = UserProject.query.all()
        return [
            {
                "id": up.id,
                "user_id": up.user_id,
                "project_id": up.project_id,
                "role_id": up.role_id,
                "team_id": up.team_id
            }
            for up in ups
        ]

    def post(self):
        data = request.get_json(force=True)
        keys = ("user_id", "project_id")
        if not all(k in data for k in keys):
            abort(400, description="Fields 'user_id' and 'project_id' required")

        # Перевірка існування звʼязаних записів:
        if not User.query.get(data["user_id"]):
            abort(404, description="User not found")
        if not Project.query.get(data["project_id"]):
            abort(404, description="Project not found")

        # role_id та team_id – не обов'язкові, але якщо передали, перевіряємо існування:
        role_id = data.get("role_id")
        if role_id is not None and not Role.query.get(role_id):
            abort(404, description="Role not found")

        team_id = data.get("team_id")
        if team_id is not None and not Team.query.get(team_id):
            abort(404, description="Team not found")

        new = UserProject(
            user_id=data["user_id"],
            project_id=data["project_id"],
            role_id=role_id,
            team_id=team_id
        )
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "user_id": new.user_id,
            "project_id": new.project_id,
            "role_id": new.role_id,
            "team_id": new.team_id
        }, 201


class UserProjectResource(Resource):
    def get(self, up_id):
        up = UserProject.query.get(up_id)
        if not up:
            abort(404, description="User_Project not found")
        return {
            "id": up.id,
            "user_id": up.user_id,
            "project_id": up.project_id,
            "role_id": up.role_id,
            "team_id": up.team_id
        }

    def put(self, up_id):
        up = UserProject.query.get(up_id)
        if not up:
            abort(404, description="User_Project not found")
        data = request.get_json(force=True)

        if "user_id" in data:
            if not User.query.get(data["user_id"]):
                abort(404, description="User not found")
            up.user_id = data["user_id"]
        if "project_id" in data:
            if not Project.query.get(data["project_id"]):
                abort(404, description="Project not found")
            up.project_id = data["project_id"]
        if "role_id" in data:
            if data["role_id"] is not None and not Role.query.get(data["role_id"]):
                abort(404, description="Role not found")
            up.role_id = data["role_id"]
        if "team_id" in data:
            if data["team_id"] is not None and not Team.query.get(data["team_id"]):
                abort(404, description="Team not found")
            up.team_id = data["team_id"]

        db.session.commit()
        return {"message": "User_Project updated"}

    def delete(self, up_id):
        up = UserProject.query.get(up_id)
        if not up:
            abort(404, description="User_Project not found")
        db.session.delete(up)
        db.session.commit()
        return {"message": "User_Project deleted"}


class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "startDate": str(t.startDate),
                "deadlineDate": str(t.deadlineDate) if t.deadlineDate else None,
                "team_id": t.team_id
            }
            for t in tasks
        ]

    def post(self):
        data = request.get_json(force=True)
        keys = ("name", "team_id")
        if not all(k in data for k in keys):
            abort(400, description="Fields 'name' and 'team_id' required")

        if not Team.query.get(data["team_id"]):
            abort(404, description="Team not found")

        new = Task(
            name=data["name"].strip(),
            description=data.get("description"),
            team_id=data["team_id"]
        )
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "name": new.name,
            "description": new.description,
            "startDate": str(new.startDate),
            "deadlineDate": str(new.deadlineDate) if new.deadlineDate else None,
            "team_id": new.team_id
        }, 201


class TaskResource(Resource):
    def get(self, task_id):
        t = Task.query.get(task_id)
        if not t:
            abort(404, description="Task not found")
        return {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "startDate": str(t.startDate),
            "deadlineDate": str(t.deadlineDate) if t.deadlineDate else None,
            "team_id": t.team_id
        }

    def put(self, task_id):
        t = Task.query.get(task_id)
        if not t:
            abort(404, description="Task not found")
        data = request.get_json(force=True)
        if "name" in data and data["name"].strip():
            t.name = data["name"].strip()
        if "description" in data:
            t.description = data["description"]
        if "deadlineDate" in data:
            t.deadlineDate = data["deadlineDate"]
        if "team_id" in data:
            if not Team.query.get(data["team_id"]):
                abort(404, description="Team not found")
            t.team_id = data["team_id"]
        db.session.commit()
        return {"message": "Task updated"}

    def delete(self, task_id):
        t = Task.query.get(task_id)
        if not t:
            abort(404, description="Task not found")
        db.session.delete(t)
        db.session.commit()
        return {"message": "Task deleted"}


#
#  2.6 Artifact
#
class ArtifactListResource(Resource):
    def get(self):
        artifacts = Artifact.query.all()
        return [
            {
                "id": a.id,
                "status": a.status,
                "comment": a.comment,
                "datetime": str(a.datetime),
                "task_id": a.task_id
            }
            for a in artifacts
        ]

    def post(self):
        data = request.get_json(force=True)
        keys = ("status", "task_id")
        if not all(k in data for k in keys):
            abort(400, description="Fields 'status' and 'task_id' required")
        if not Task.query.get(data["task_id"]):
            abort(404, description="Task not found")

        new = Artifact(
            status=data["status"].strip(),
            comment=data.get("comment"),
            task_id=data["task_id"]
        )
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "status": new.status,
            "comment": new.comment,
            "datetime": str(new.datetime),
            "task_id": new.task_id
        }, 201


class ArtifactResource(Resource):
    def get(self, artifact_id):
        a = Artifact.query.get(artifact_id)
        if not a:
            abort(404, description="Artifact not found")
        return {
            "id": a.id,
            "status": a.status,
            "comment": a.comment,
            "datetime": str(a.datetime),
            "task_id": a.task_id
        }

    def put(self, artifact_id):
        a = Artifact.query.get(artifact_id)
        if not a:
            abort(404, description="Artifact not found")
        data = request.get_json(force=True)
        if "status" in data and data["status"].strip():
            a.status = data["status"].strip()
        if "comment" in data:
            a.comment = data["comment"]
        if "task_id" in data:
            if not Task.query.get(data["task_id"]):
                abort(404, description="Task not found")
            a.task_id = data["task_id"]
        db.session.commit()
        return {"message": "Artifact updated"}

    def delete(self, artifact_id):
        a = Artifact.query.get(artifact_id)
        if not a:
            abort(404, description="Artifact not found")
        db.session.delete(a)
        db.session.commit()
        return {"message": "Artifact deleted"}


#
#  2.7 Action
#
class ActionListResource(Resource):
    def get(self):
        acts = Action.query.all()
        return [{"id": a.id, "action": a.action} for a in acts]

    def post(self):
        data = request.get_json(force=True)
        if "action" not in data or not data["action"].strip():
            abort(400, description="Field 'action' required")
        if Action.query.filter_by(action=data["action"].strip()).first():
            abort(409, description="Action already exists")

        new = Action(action=data["action"].strip())
        db.session.add(new)
        db.session.commit()
        return {"id": new.id, "action": new.action}, 201


class ActionResource(Resource):
    def get(self, action_id):
        a = Action.query.get(action_id)
        if not a:
            abort(404, description="Action not found")
        return {"id": a.id, "action": a.action}

    def put(self, action_id):
        a = Action.query.get(action_id)
        if not a:
            abort(404, description="Action not found")
        data = request.get_json(force=True)
        if "action" in data and data["action"].strip():
            if Action.query.filter(Action.action == data["action"].strip(), Action.id != action_id).first():
                abort(409, description="Another action with this name already exists")
            a.action = data["action"].strip()
        db.session.commit()
        return {"message": "Action updated"}

    def delete(self, action_id):
        a = Action.query.get(action_id)
        if not a:
            abort(404, description="Action not found")
        db.session.delete(a)
        db.session.commit()
        return {"message": "Action deleted"}


class RoleActionListResource(Resource):
    def get(self):
        ras = RoleAction.query.all()
        return [
            {
                "id": ra.id,
                "role_id": ra.role_id,
                "action_id": ra.action_id
            }
            for ra in ras
        ]

    def post(self):
        data = request.get_json(force=True)
        keys = ("role_id", "action_id")
        if not all(k in data for k in keys):
            abort(400, description="Fields 'role_id' and 'action_id' required")
        if not Role.query.get(data["role_id"]):
            abort(404, description="Role not found")
        if not Action.query.get(data["action_id"]):
            abort(404, description="Action not found")

        new = RoleAction(role_id=data["role_id"], action_id=data["action_id"])
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "role_id": new.role_id,
            "action_id": new.action_id
        }, 201


class RoleActionResource(Resource):
    def get(self, ra_id):
        ra = RoleAction.query.get(ra_id)
        if not ra:
            abort(404, description="Role_Action not found")
        return {"id": ra.id, "role_id": ra.role_id, "action_id": ra.action_id}

    def put(self, ra_id):
        ra = RoleAction.query.get(ra_id)
        if not ra:
            abort(404, description="Role_Action not found")
        data = request.get_json(force=True)
        if "role_id" in data:
            if not Role.query.get(data["role_id"]):
                abort(404, description="Role not found")
            ra.role_id = data["role_id"]
        if "action_id" in data:
            if not Action.query.get(data["action_id"]):
                abort(404, description="Action not found")
            ra.action_id = data["action_id"]
        db.session.commit()
        return {"message": "Role_Action updated"}

    def delete(self, ra_id):
        ra = RoleAction.query.get(ra_id)
        if not ra:
            abort(404, description="Role_Action not found")
        db.session.delete(ra)
        db.session.commit()
        return {"message": "Role_Action deleted"}


#
#  2.9 Event
#
class EventListResource(Resource):
    def get(self):
        evs = Event.query.all()
        return [
            {
                "id": e.id,
                "user_id": e.user_id,
                "role_id": e.role_id,
                "action": e.action,
                "datetime": str(e.datetime)
            }
            for e in evs
        ]

    def post(self):
        data = request.get_json(force=True)
        keys = ("user_id", "role_id", "action")
        if not all(k in data for k in keys):
            abort(400, description="Fields 'user_id', 'role_id', and 'action' required")
        if not User.query.get(data["user_id"]):
            abort(404, description="User not found")
        if not Role.query.get(data["role_id"]):
            abort(404, description="Role not found")

        new = Event(
            user_id=data["user_id"],
            role_id=data["role_id"],
            action=data["action"].strip()
        )
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "user_id": new.user_id,
            "role_id": new.role_id,
            "action": new.action,
            "datetime": str(new.datetime)
        }, 201


class EventResource(Resource):
    def get(self, event_id):
        e = Event.query.get(event_id)
        if not e:
            abort(404, description="Event not found")
        return {
            "id": e.id,
            "user_id": e.user_id,
            "role_id": e.role_id,
            "action": e.action,
            "datetime": str(e.datetime)
        }

    def put(self, event_id):
        e = Event.query.get(event_id)
        if not e:
            abort(404, description="Event not found")
        data = request.get_json(force=True)
        if "user_id" in data:
            if not User.query.get(data["user_id"]):
                abort(404, description="User not found")
            e.user_id = data["user_id"]
        if "role_id" in data:
            if not Role.query.get(data["role_id"]):
                abort(404, description="Role not found")
            e.role_id = data["role_id"]
        if "action" in data and data["action"].strip():
            e.action = data["action"].strip()
        db.session.commit()
        return {"message": "Event updated"}

    def delete(self, event_id):
        e = Event.query.get(event_id)
        if not e:
            abort(404, description="Event not found")
        db.session.delete(e)
        db.session.commit()
        return {"message": "Event deleted"}


@app.route("/")
def index():
    return {"message": "API is working"}


api.add_resource(ProjectListResource, '/projects')
api.add_resource(ProjectResource,     '/projects/<int:project_id>')

api.add_resource(TeamListResource,    '/teams')
api.add_resource(TeamResource,        '/teams/<int:team_id>')

api.add_resource(RoleListResource,    '/roles')
api.add_resource(RoleResource,        '/roles/<int:role_id>')

api.add_resource(UserProjectListResource, '/user_projects')
api.add_resource(UserProjectResource,     '/user_projects/<int:up_id>')

api.add_resource(TaskListResource,    '/tasks')
api.add_resource(TaskResource,        '/tasks/<int:task_id>')

api.add_resource(ArtifactListResource, '/artifacts')
api.add_resource(ArtifactResource,     '/artifacts/<int:artifact_id>')

api.add_resource(ActionListResource,  '/actions')
api.add_resource(ActionResource,      '/actions/<int:action_id>')

api.add_resource(RoleActionListResource, '/role_actions')
api.add_resource(RoleActionResource,     '/role_actions/<int:ra_id>')

api.add_resource(EventListResource,   '/events')
api.add_resource(EventResource,       '/events/<int:event_id>')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
