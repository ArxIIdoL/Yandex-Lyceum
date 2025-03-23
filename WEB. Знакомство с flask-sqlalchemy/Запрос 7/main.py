def main():
    db_name = input()
    global_init(db_name)
    db_sess = create_session()
    for user in db_sess.query(User).filter(User.age < 21, User.address.like("%_1")):
        user.address = "module_3"
    db_sess.commit()


if __name__ == '__main__':
    main()
