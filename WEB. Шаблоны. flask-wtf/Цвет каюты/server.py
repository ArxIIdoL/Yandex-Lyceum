from flask import Flask, render_template
from random import choice

app = Flask(__name__)
app.config["SECRET_KEY"] = "nadoeli_zadachi"


@app.route("/")
def task_name():
    return "Цвет каюты"


@app.route("/table/<gender>/<int:age>")
def table(gender, age):
    fem_colors, male_colors = ("#ffa500", "#ff4500"), ("#00ffff", "#87cefa")
    param = {
        "title": "Цвет каюты",
        "wall_color": choice({"male": male_colors, "female": fem_colors}[gender]),
        "is_adult": age > 21
    }
    return render_template("cabin color.html", **param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
