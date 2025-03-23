def main():
    db_name = input()
    global_init(db_name)
    db_sess = create_session()
    for user in db_sess.query(User).filter((User.position.like("%chief%")) | (User.position.like("%middle%"))):
        print(f"{user} {user.position}")


if __name__ == '__main__':
    main()