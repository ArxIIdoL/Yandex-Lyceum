# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "Отбор астронавтов"


@app.route("/astronaut_selection", methods=("POST", "GET"))
def astronaut_selection():
    if request.method == "GET":
        return render_template("astronaut_selection.html")
    elif request.method == "POST":
        return "OK"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
