from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime

from data import db_session
from data.jobs import Jobs
from data.users import User
from data.department import Department
from forms.job import AddJobForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
DB_NAME = "db/mars_explorer.db"


def main():
    db_session.global_init(DB_NAME)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route("/")
def index():
    if current_user.is_authenticated:
        db_session.global_init(DB_NAME)
        db_sess = db_session.create_session()
        param = {"title": "Работы", "jobs": db_sess.query(Jobs).all()}
        return render_template("index.html", **param)
    else:
        return render_template("index.html", title="Please work")


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_session.global_init(DB_NAME)
        db_sess = db_session.create_session()
        try:
            if db_sess.query(User).filter(User.name == form.team_leader.data.split()[1],
                                          User.surname == form.team_leader.data.split()[0]).first() is None:
                return render_template('add_job.html', title='Add_job', form=form,
                                       message="Такого астронавта не существует")
            for collaborator in form.collaborators.data.split(', '):
                exist = False
                for user in db_sess.query(User).all():
                    if int(collaborator) == user.id:
                        exist = True
                        break
                if not exist:
                    return render_template('add_job.html', title='Add_job', form=form,
                                           message=f"Такой {collaborator} id помощника не найден")
            if form.start_date.data != '':
                date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            if form.end_date.data != '':
                date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(e)
            return render_template('add_job.html', title='Add_job', form=form,
                                   message="Ошибка заполнения данных")
        new_job = Jobs(
            team_leader=db_sess.query(User).filter(User.name == form.team_leader.data.split()[1],
                                          User.surname == form.team_leader.data.split()[0]).first().id,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=", ".join(sorted(form.collaborators.data.split(', '))),
            start_date=(None if form.start_date.data == '' else form.start_date.data),
            end_date=(None if form.end_date.data == '' else form.end_date.data),
            is_finished=form.is_finished.data
        )
        db_sess.add(new_job)
        db_sess.commit()
        return redirect('/')

    return render_template('add_job.html', title='Регистрация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация в системе Mars One', form=form)


if __name__ == '__main__':
    main()
