def main():
    db_name = input()
    global_init(db_name)
    db_sess = create_session()
    jobs_list = sorted([(jobs.team_leader, len(jobs.collaborators.split(", "))) for jobs in db_sess.query(Jobs).all()],
                       key=lambda x: x[1], reverse=True)
    team_leaders_id = [values[0] for values in jobs_list if max(jobs_list, key=lambda x: x[1])[1] == values[1]]
    for user in db_sess.query(User).filter(User.id.in_(team_leaders_id)):
        print(f"{user.name} {user.surname}")


if __name__ == '__main__':
    main()