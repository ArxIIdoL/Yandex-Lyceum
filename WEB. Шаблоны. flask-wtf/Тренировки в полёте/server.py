from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index/<title>")
def index(title):
    return render_template('base.html', title=title)


@app.route("/training/<prof>")
def training(prof):
    is_engineer = True if "инженер" in prof.lower() or "строитель" in prof.lower() else False
    return render_template('training.html', title="Тренировки в полёте", engineer=is_engineer)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
