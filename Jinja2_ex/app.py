from flask import Flask
from flask import Flask, render_template,abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

BASE_DIR = Path(__file__).parent


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'flask.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32),nullable=False,unique =True)
    name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=True)
    birth_date = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(32), nullable=True)

    def __init__(self, login, name, last_name, surname, birth_date, phone):
        self.login = login
        self.name = name
        self.last_name = last_name
        self.surname = surname
        self.birth_date = birth_date
        self.phone = phone
        

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "name": self.name,
            "last_name": self.last_name,
            "surname": self.surname,
            "birth_date": self.birth_date,
            "phone": self.phone
            
            
        }

    def __repr__(self):
        return f"UserModel {vars(self)}"

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/names")
def names():
    user_name = []
    users = UserModel.query.all()
    for user in users:
        user_name.append(user.name)
    # with open("files/names.txt", encoding="utf-8") as f:
    #     for raw_line in f:
    #         names.append(raw_line.strip())
    
    return render_template('names.html', **{'names': user_name})


@app.route("/table")
def table():
    # entities = []
    # with open("files/humans.txt", encoding="utf-8") as tables:
    #     for raw_line in tables:
    #         data = raw_line.strip().split(';')
    #         entities.append({'last_name': data[0],
    #             'name': data[1], 'surname': data[2]})
    users = UserModel.query.all()
    return render_template('table.html', tables=users)


@app.route('/users')
def users_list():
    users = UserModel.query.all()
    # entities = []
    # with open("files/users.txt", encoding="utf-8") as tables:
    #     for raw_line in tables:
    #         data = raw_line.strip().split(';')
    #         entities.append(dict(
    #             zip(('login', 'last_name', 'name', 'surname', 'birth_date', 'phone'), data)))
    return render_template('users_list.html', users_info = users)


@app.route('/users/<login>')
def users_login(login):
    get_user = UserModel.query.filter_by(login=login).one()
    if not get_user:
        return abort(404, f"Пользователе с логином {login} не найден")
    # item = None
    # with open("files/users.txt", encoding="utf-8") as tables:
    #     for raw_line in tables:
    #         if login in raw_line:
    #             data = raw_line.strip().split(';')
    #             item = dict(
    #                 zip(('login', 'last_name', 'name', 'surname', 'birth_date', 'phone'), data))
    #             break
    # if item is None:
    #    return abort(404,f"Пользователе с логином {login} не найден")
    return render_template('user_item.html', user_info = get_user)



@app.route("/about")
def about():
    return "О нас"


if __name__ == "__main__":
    app.run(host='192.168.10.43',debug=True)
