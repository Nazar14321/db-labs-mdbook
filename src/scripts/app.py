from flask import Flask, request, abort
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)

db  = SQLAlchemy(app)
api = Api(app)



class Project(db.Model):
    __tablename__ = 'Project'
    id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name  = db.Column(db.Text, nullable=False)


    teams = db.relationship('Team', backref='project', lazy='dynamic')


class Team(db.Model):
    __tablename__ = 'Team'
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.Text, nullable=False)
    project_id = db.Column(
                    db.Integer,
                    db.ForeignKey('Project.id', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False
                 )


    users = db.relationship('User', backref='team', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'User'
    id       = db.Column(db.CHAR(36), primary_key=True, default=db.func.UUID())


    nickname = db.Column(db.String(255), nullable=False, unique=True)
    email    = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    photo    = db.Column(db.Text, nullable=True)

    team_id  = db.Column(
                  db.Integer,
                  db.ForeignKey('Team.id', ondelete='CASCADE', onupdate='CASCADE'),
                  nullable=False
               )



class ProjectListResource(Resource):
    def get(self):
        projects = Project.query.all()
        return [{"id": p.id, "name": p.name} for p in projects]

    def post(self):
        data = request.get_json(force=True)
        if "name" not in data or not data["name"].strip():
            abort(400, description="Field 'name' is required")
        new = Project(name=data["name"].strip())
        db.session.add(new)
        db.session.commit()
        return {"id": new.id, "name": new.name}, 201


class ProjectResource(Resource):
    def get(self, project_id):
        p = Project.query.get(project_id)
        if not p:
            abort(404, description="Project not found")
        return {"id": p.id, "name": p.name}

    def put(self, project_id):
        p = Project.query.get(project_id)
        if not p:
            abort(404, description="Project not found")
        data = request.get_json(force=True)
        if "name" in data and data["name"].strip():
            p.name = data["name"].strip()
        db.session.commit()
        return {"message": "Project updated"}

    def delete(self, project_id):
        p = Project.query.get(project_id)
        if not p:
            abort(404, description="Project not found")
        db.session.delete(p)
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
            abort(400, description="Field 'name' is required")
        if "project_id" not in data:
            abort(400, description="Field 'project_id' is required")
        if not Project.query.get(data["project_id"]):
            abort(404, description="Project not found")

        new = Team(
            name=data["name"].strip(),
            project_id=data["project_id"]
        )
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "name": new.name,
            "project_id": new.project_id
        }, 201


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


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [
            {
                "id": u.id,
                "nickname": u.nickname,
                "email": u.email,
                "photo": u.photo,
                "team_id": u.team_id
            }
            for u in users
        ]

    def post(self):
        data = request.get_json(force=True)
        required = ("nickname", "email", "password", "team_id")
        if not all(k in data for k in required):
            abort(400, description="Fields 'nickname','email','password','team_id' are required")

        # Перевірка унікальності:
        if User.query.filter_by(email=data["email"].strip()).first():
            abort(409, description="User with this email already exists")
        if User.query.filter_by(nickname=data["nickname"].strip()).first():
            abort(409, description="User with this nickname already exists")

        # Перевірка наявності команди:
        if not Team.query.get(data["team_id"]):
            abort(404, description="Team not found")

        new = User(
            nickname=data["nickname"].strip(),
            email=data["email"].strip(),
            password=data["password"],  # У реальному проєкті: зберігати лише хеш!
            photo=data.get("photo"),
            team_id=data["team_id"]
        )
        db.session.add(new)
        db.session.commit()
        return {
            "id": new.id,
            "nickname": new.nickname,
            "email": new.email,
            "photo": new.photo,
            "team_id": new.team_id
        }, 201


class UserResource(Resource):
    def get(self, user_id):
        u = User.query.get(user_id)
        if not u:
            abort(404, description="User not found")
        return {
            "id": u.id,
            "nickname": u.nickname,
            "email": u.email,
            "photo": u.photo,
            "team_id": u.team_id
        }

    def put(self, user_id):
        u = User.query.get(user_id)
        if not u:
            abort(404, description="User not found")
        data = request.get_json(force=True)

        if "nickname" in data:
            candidate = data["nickname"].strip()
            if User.query.filter(User.nickname == candidate, User.id != user_id).first():
                abort(409, description="Another user with this nickname already exists")
            u.nickname = candidate

        if "email" in data:
            candidate = data["email"].strip()
            if User.query.filter(User.email == candidate, User.id != user_id).first():
                abort(409, description="Another user with this email already exists")
            u.email = candidate

        if "password" in data:
            u.password = data["password"]

        if "photo" in data:
            u.photo = data["photo"]  # може бути None

        if "team_id" in data:
            if not Team.query.get(data["team_id"]):
                abort(404, description="Team not found")
            u.team_id = data["team_id"]

        db.session.commit()
        return {"message": "User updated"}

    def delete(self, user_id):
        u = User.query.get(user_id)
        if not u:
            abort(404, description="User not found")
        db.session.delete(u)
        db.session.commit()
        return {"message": "User deleted"}



@app.route("/")
def index():
    return {"message": "API is working"}

api.add_resource(ProjectListResource, '/projects')
api.add_resource(ProjectResource,     '/projects/<int:project_id>')

api.add_resource(TeamListResource,    '/teams')
api.add_resource(TeamResource,        '/teams/<int:team_id>')

api.add_resource(UserListResource,    '/users')
api.add_resource(UserResource,        '/users/<string:user_id>')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
