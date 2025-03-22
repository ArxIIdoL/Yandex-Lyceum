from flask import Flask

from data.jobs import Jobs
from data.users import User
from data import db_session
from json import load
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.now()
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()


if __name__ == '__main__':
    main()
