from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "nadoeli_zadachi"


@app.route("/")
def task_name():
    return "Автоматический ответ"


@app.route("/answer")
@app.route('/auto_answer')
def auto_answer():
    param = {
        "title": "анкета",
        "surname": "Watny",
        "name": "Mark",
        "education": "выше среднего",
        "profession": "штурман марсохода",
        "sex": "мужской",
        "motivation": "Всегда мечтал застрять на Марсе",
        "ready": True
    }
    return render_template('auto_answer.html', **param)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
