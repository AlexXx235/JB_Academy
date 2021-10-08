import db_tools
import datetime


def menu(session):
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
          "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    choice = input()
    if choice == '1':
        show_today_tasks(session)
    elif choice == '2':
        show_week_tasks(session)
    elif choice == '3':
        show_all_tasks(session)
    elif choice == '4':
        show_missed_tasks(session)
    elif choice == '5':
        add_task(session)
    elif choice == '6':
        delete_task(session)
    elif choice == '0':
        print('Bye!')
        exit()
    else:
        print('Try again!')


def show_missed_tasks(session):
    today = datetime.datetime.today().date()
    tasks = session.query(db_tools.Task).filter(db_tools.Task.deadline < today).all()
    if not tasks:
        print('Nothing is missed!')
    else:
        print('Missed tasks:')
        for number, task in enumerate(tasks):
            print(f'{number + 1}. {task.task}. {task.deadline.day} {task.deadline.strftime("%b")}')
    print('')


def show_today_tasks(session):
    tasks = session.query(db_tools.Task)
    tasks = tasks.filter(db_tools.Task.deadline == datetime.datetime.today().date()).all()
    print('Today:')
    if not tasks:
        print('Nothing to do!')
    else:
        for number, task in enumerate(tasks):
            print(f'{number + 1}.', task.task)
    print('')


def show_week_tasks(session):
    weekdays = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    current_date = datetime.datetime.today().date()
    all_tasks = session.query(db_tools.Task)
    for delta in range(0,7):
        current_date = (datetime.datetime.today() + datetime.timedelta(days=delta)).date()
        weekday = current_date.weekday()
        daily_tasks = all_tasks.filter(db_tools.Task.deadline == current_date).all()
        print(f'\n{weekdays[weekday]} {current_date.day} {current_date.strftime("%b")}:')
        if not daily_tasks:
            print('Nothing to do!')
        else:
            for number, task in enumerate(daily_tasks):
                print(f'{number + 1}. {task.task}')


def show_all_tasks(session):
    tasks = session.query(db_tools.Task).order_by(db_tools.Task.deadline).all()
    print('All tasks:')
    if not tasks:
        print('Nothing to do!')
    else:
        for number, task in enumerate(tasks):
            print(f'{number + 1}. {task.task}. {task.deadline.day} {task.deadline.strftime("%b")}')
    print('')


def add_task(session):
    task_description = input('Enter task\n')
    deadline = list(map(int, input('Enter deadline\n').split('-')))
    deadline = datetime.datetime(deadline[0], deadline[1], deadline[2])
    new_task = db_tools.Task(
        task=task_description,
        deadline=deadline
    )
    session.add(new_task)
    session.commit()
    print('The task has been added!')


def delete_task(session):
    tasks = session.query(db_tools.Task).all()
    if not tasks:
        print('Nothing to delete')
    else:
        print('Choose the number of the task you want to delete:')
        for number, task in enumerate(tasks):
            print(f'{number + 1}. {task.task}. {task.deadline.day} {task.deadline.strftime("%b")}')
        num_to_delete = int(input())
        session.delete(tasks[num_to_delete - 1])
    session.commit()

if __name__ == '__main__':
    session = db_tools.session
    while True:
        menu(session)