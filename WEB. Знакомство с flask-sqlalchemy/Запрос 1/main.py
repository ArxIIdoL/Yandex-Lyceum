def main():
    db_name = input()
    global_init(db_name)
    db_sess = create_session()
    for user in db_sess.query(User).filter(User.address.like("%_1")):
        print(user)


if __name__ == '__main__':
    main()
