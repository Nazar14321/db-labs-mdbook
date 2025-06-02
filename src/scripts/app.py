from flask import Flask, request, abort
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    __tablename__ = 'User'
    id       = db.Column(db.CHAR(36), primary_key=True, default=db.func.UUID())
    nickname = db.Column(db.Text, nullable=False, unique=True)
    email    = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    photo    = db.Column(db.Text, nullable=True)


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        result = []
        for u in users:
            result.append({
                "id": u.id,
                "nickname": u.nickname,
                "email": u.email,
                "photo": u.photo
            })
        return result

    def post(self):
        data = request.get_json(force=True)
        if not all(k in data for k in ("nickname", "email", "password")):
            abort(400, description="Missing fields: nickname, email, password required")

        if User.query.filter_by(email=data["email"]).first():
            abort(409, description="User with this email already exists")
        if User.query.filter_by(nickname=data["nickname"]).first():
            abort(409, description="User with this nickname already exists")

        new_user = User(
            nickname=data["nickname"],
            email=data["email"],
            password=data["password"],
            photo=data.get("photo")
        )
        db.session.add(new_user)
        db.session.commit()


        return {
            "id": new_user.id,
            "nickname": new_user.nickname,
            "email": new_user.email,
            "photo": new_user.photo
        }, 201


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, description="User not found")
        return {
            "id": user.id,
            "nickname": user.nickname,
            "email": user.email,
            "photo": user.photo
        }

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, description="User not found")

        data = request.get_json(force=True)
        if "nickname" in data:
            user.nickname = data["nickname"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = data["password"]
        if "photo" in data:
            user.photo = data["photo"]

        db.session.commit()
        return {"message": "User updated"}

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            abort(404, description="User not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}
@app.route("/")
def index():
    return {"message": "Hello i`m working"}

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<string:user_id>')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)