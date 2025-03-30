from datetime import datetime

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from sqlalchemy import orm

from data import db_session, users_resource, jobs_resource
from data.category import Category
from data.department import Department
from data.jobs import Jobs
from data.users import User
from forms.department import DepartmentForm
from forms.job import JobForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app, catch_all_404s=True)


def main():
    db_session.global_init("db/mars_explorer.db")
    api.add_resource(users_resource.UserListResource, '/api/v2/users')
    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
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
        db_sess = db_session.create_session()
        param = {
            "title": "Работы",
            "jobs": db_sess.query(Jobs).options(orm.joinedload(Jobs.categories)).all(),
            "captain": db_sess.query(User).filter(User.id == 1).first()
        }
        return render_template("index.html", **param)
    else:

        db_sess = db_session.create_session()
        param = {
            "title": "Работы",
            "jobs": db_sess.query(Jobs).options(orm.joinedload(Jobs.categories)).all()
        }
        return render_template("index.html", **param)


@login_required
@app.route("/departments")
def departments():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        param = {
            "title": "Департаменты",
            "departments": db_sess.query(Department).all(),
            "captain": db_sess.query(User).filter(User.id == 1).first()
        }
        return render_template("departments.html", **param)
    return render_template("departments.html")


@login_required
@app.route("/add_department", methods=['GET', 'POST'])
def add_department():
    if not current_user.is_authenticated:
        return redirect("/")
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            if db_sess.query(User).filter(User.name == form.chief.data.split()[1],
                                          User.surname == form.chief.data.split()[0]).first() is None:
                return render_template('department.html', title='Add department', form=form,
                                       message="Такого астронавта не существует", type="add")
            for member in form.members.data.split(', '):
                exist = False
                for user in db_sess.query(User).all():
                    if int(member) == user.id:
                        exist = True
                        break
                if not exist:
                    return render_template('department.html', title='Add department', form=form,
                                           message=f"Такой {member} id сотрудника не найден", type="add")
        except Exception as e:
            print(e)
            return render_template('department.html', title='Add job', form=form,
                                   message="Ошибка заполнения данных", type="add")
        new_department = Department(
            title=form.title.data,
            chief=db_sess.query(User).filter(User.name == form.chief.data.split()[1],
                                             User.surname == form.chief.data.split()[0]).first().id,
            members=", ".join(sorted(form.members.data.split(', '))),
            email=form.email.data
        )
        db_sess.add(new_department)
        db_sess.commit()
        return redirect('/departments')

    return render_template('department.html', title='Add department', form=form, type="add")


@app.route('/department_delete/<int:department_id>', methods=['GET', 'POST'])
@login_required
def department_delete(department_id):
    if not current_user.is_authenticated:
        return redirect("/departments")
    db_sess = db_session.create_session()
    captain = db_sess.query(User).filter(User.id == 1).first()
    department = (
        db_sess.query(Department).filter(Department.id == department_id).first() if current_user == captain else
        db_sess.query(Department).filter
        (Department.user2 == current_user, Department.id == department_id).first())
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/edit_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        captain = db_sess.query(User).filter(User.id == 1).first()
        department = (
            db_sess.query(Department).filter(Department.id == department_id).first() if current_user == captain else
            db_sess.query(Department).filter
            (Department.user2 == current_user, Department.id == department_id).first())
        if department:
            try:
                if db_sess.query(User).filter(User.name == form.chief.data.split()[1],
                                              User.surname == form.chief.data.split()[0]).first() is None:
                    return render_template('department.html', title='Edit department', form=form,
                                           message="Такого астронавта не существует", type="edit")
                for members in form.members.data.split(', '):
                    exist = False
                    for user in db_sess.query(User).all():
                        if int(members) == user.id:
                            exist = True
                            break
                    if not exist:
                        return render_template('department.html', title='Edit department', form=form,
                                               message=f"Такой {members} id помощника не найден", type="edit")
            except Exception as e:
                print(e)
                return render_template('department.html', title='Edit department', form=form,
                                       message="Ошибка заполнения данных", type="edit")
            department.title = form.title.data
            department.chief = db_sess.query(User).filter(User.name == form.chief.data.split()[1],
                                                          User.surname == form.chief.data.split()[0]).first().id
            department.members = ", ".join(sorted(form.members.data.split(', ')))
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html', title='Редактирование департамента', form=form, type="edit")


@app.route('/job_delete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_delete(job_id):
    if not current_user.is_authenticated:
        return redirect("/")
    db_sess = db_session.create_session()
    captain = db_sess.query(User).filter(User.id == 1).first()
    job = (db_sess.query(Jobs).filter(Jobs.id == job_id).first() if current_user == captain else
           db_sess.query(Jobs).filter
           (Jobs.user == current_user, Jobs.id == job_id).first())
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        captain = db_sess.query(User).filter(User.id == 1).first()
        edit_job = (db_sess.query(Jobs).filter(Jobs.id == job_id).first() if current_user == captain else
                    db_sess.query(Jobs).filter
                    (Jobs.user == current_user, Jobs.id == job_id).first())
        if edit_job:
            try:
                if db_sess.query(User).filter(User.name == form.team_leader.data.split()[1],
                                              User.surname == form.team_leader.data.split()[0]).first() is None:
                    return render_template('job.html', title='Edit job', form=form,
                                           message="Такого астронавта не существует", type="edit")
                for form_category in form.categories.data.split(', '):
                    exist = False
                    for db_category in db_sess.query(Category).all():
                        if form_category == db_category.name:
                            exist = True
                            break
                    if not exist:
                        return render_template('job.html', title='Edit job', form=form,
                                               message=f'Категория "{form_category}" не найдена', type="edit")
                for collaborator in form.collaborators.data.split(', '):
                    exist = False
                    for user in db_sess.query(User).all():
                        if int(collaborator) == user.id:
                            exist = True
                            break
                    if not exist:
                        return render_template('job.html', title='Edit job', form=form,
                                               message=f"Такой {collaborator} id помощника не найден", type="edit")
                if form.start_date.data != '':
                    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
                if form.end_date.data != '':
                    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(e)
                return render_template('job.html', title='Edit job', form=form,
                                       message="Ошибка заполнения данных", type="edit")
            edit_job.team_leader = db_sess.query(User).filter(User.name == form.team_leader.data.split()[1],
                                                              User.surname == form.team_leader.data.split()[
                                                                  0]).first().id
            edit_job.job = form.job.data
            edit_job.work_size = form.work_size.data
            edit_job.collaborators = ", ".join(sorted(form.collaborators.data.split(', ')))
            edit_job.start_date = (None if form.start_date.data == '' else form.start_date.data)
            edit_job.end_date = (None if form.end_date.data == '' else form.end_date.data)
            edit_job.is_finished = form.is_finished.data
            edit_job.categories.clear()
            for category_name in form.categories.data.split(', '):
                category = db_sess.query(Category).filter(Category.name == category_name).first()
                category.jobs.append(edit_job)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html', title='Редактирование работы', form=form, type="edit")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    if not current_user.is_authenticated:
        return redirect("/")
    form = JobForm()
    if form.validate_on_submit():

        db_sess = db_session.create_session()
        try:
            if db_sess.query(User).filter(User.name == form.team_leader.data.split()[1],
                                          User.surname == form.team_leader.data.split()[0]).first() is None:
                return render_template('job.html', title='Add job', form=form,
                                       message="Такого астронавта не существует", type="add")
            for form_category in form.categories.data.split(', '):
                exist = False
                for db_category in db_sess.query(Category).all():
                    if form_category == db_category.name:
                        exist = True
                        break
                if not exist:
                    return render_template('job.html', title='Add job', form=form,
                                           message=f'Категория "{form_category}" не найдена', type="add")
            for collaborator in form.collaborators.data.split(', '):
                exist = False
                for user in db_sess.query(User).all():
                    if int(collaborator) == user.id:
                        exist = True
                        break
                if not exist:
                    return render_template('job.html', title='Add job', form=form,
                                           message=f"Такой {collaborator} id помощника не найден", type="add")
            if form.start_date.data != '':
                date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            if form.end_date.data != '':
                date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(e)
            return render_template('job.html', title='Add job', form=form,
                                   message="Ошибка заполнения данных", type="add")
        new_job = Jobs(
            team_leader=db_sess.query(User).filter(User.name == form.team_leader.data.split()[1],
                                                   User.surname == form.team_leader.data.split()[0]).first().id,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=", ".join(sorted(form.collaborators.data.split(', '))),
            start_date=(None if form.start_date.data == '' else form.start_date.data),
            end_date=(None if form.end_date.data == '' else form.end_date.data),
            is_finished=form.is_finished.data,
        )
        for category_name in form.categories.data.split(', '):
            category = db_sess.query(Category).filter(Category.name == category_name).first()
            category.jobs.append(new_job)
        db_sess.add(new_job)
        db_sess.commit()
        return redirect('/')

    return render_template('job.html', title='Add job', form=form, type="add")


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
