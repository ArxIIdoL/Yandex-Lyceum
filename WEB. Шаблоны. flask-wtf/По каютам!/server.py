from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "nadoeli_zadachi"


@app.route("/")
def task_name():
    return "По каютам!"


@app.route("/distribution")
def distribution():
    members = (
        "Ридли Скотт",
        "Энди Уир",
        "Марк Уотни"
    )
    return render_template("distribution.html", members=members, title="По каютам!")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
