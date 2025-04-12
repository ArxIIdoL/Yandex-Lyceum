from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route("/")
def root():
    return "Загрузка файла"


@app.route("/load_photo", methods=("POST", "GET"))
def load_photo():
    if request.method == "GET":
        return render_template("load_photo.html")
    elif request.method == "POST":
        f = request.files["file"]
        f.save("static/img/photo.png")
        return "OK"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
