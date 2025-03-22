from flask import Flask

from data.jobs import Jobs
from data.users import User
from data import db_session
from json import load

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    with open("data/colonists.json") as json_file:
        data = load(json_file)
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    for colonist_data in data:
        user = User()
        user.surname = colonist_data["surname"]
        user.name = colonist_data["name"]
        user.age = colonist_data["age"]
        user.position = colonist_data["position"]
        user.speciality = colonist_data["speciality"]
        user.address = colonist_data["address"]
        user.email = colonist_data["email"]
        db_sess.add(user)
        db_sess.commit()


if __name__ == '__main__':
    main()
