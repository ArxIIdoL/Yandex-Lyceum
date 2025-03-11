from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def task_name():
    return "Список профессий"


@app.route('/list_prof/<list>')
def list_of_professions(list):
    mars_mission_professions = [
        'астронавт',
        'инженер-механик',
        'биолог',
        'геолог',
        'медицинский работник',
        'инженер-электрик',
        'программист',
        'специалист по связи',
        'психолог',
        'агроном'
    ]
    is_labeled = True if list == 'ul' else False
    return render_template('base.html', title='Список профессий',
                           labeled=is_labeled, professions=mars_mission_professions)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
