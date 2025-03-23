def main():
    db_name = input()
    global_init(db_name)
    db_sess = create_session()
    for jobs in db_sess.query(Jobs).filter(Jobs.work_size < 20, Jobs.is_finished == 0):
        print(f"{jobs}")


if __name__ == '__main__':
    main()