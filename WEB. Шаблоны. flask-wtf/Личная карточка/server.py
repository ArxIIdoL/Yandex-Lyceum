# -*- coding: utf-8 -*-
from json import load
from random import randrange

from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "nadoeli_zadachi"


@app.route("/")
def task_name():
    return "Личная карточка"


@app.route("/member")
def member():
    with open('templates/members.json', encoding='UTF-8-SIG') as file:
        data = load(file)
    random_member_data = data["members"][randrange(len(data["members"]))]
    param = {
        "title": "Личная карточка",
        "fullname": f'{random_member_data["surname"]} {random_member_data["name"]}',
        "image_path": random_member_data["image_path"],
        "jobs": ", ".join(sorted(random_member_data["jobs"]))
    }
    return render_template("member.html", **param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
