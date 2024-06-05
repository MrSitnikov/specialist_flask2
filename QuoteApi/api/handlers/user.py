from api import app, db, request,multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema

@app.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = UserModel.query.get(user_id)
    if user is None:
        return {"Error": f"Users id={user_id} not found"}, 404
    return user_schema.dump(user),200

@app.route("/users")
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users),200


@app.post("/users")
@multi_auth.login_required
def create_user():
    user_data = request.json
    #print('user=', auth.current_user()) #текущий пользователь
    user = UserModel(**user_data)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201


@app.delete("/user/<int:user_id>")
@multi_auth.login_required
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User: id={user_id} delete"}, 200
    return {"Error": f"Users id={user_id} not found"}, 404
