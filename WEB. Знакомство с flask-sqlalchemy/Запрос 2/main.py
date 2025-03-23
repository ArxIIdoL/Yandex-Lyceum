def main():
    db_name = input()
    global_init(db_name)
    db_sess = create_session()
    for user in db_sess.query(User).filter(
            User.address.like("%_1"), User.speciality.notilike("%engineer%"), User.position.notilike("%engineer%")):
        print(user.id)


if __name__ == '__main__':
    main()