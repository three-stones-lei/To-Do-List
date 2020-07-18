# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

Base.metadata.create_all(engine)

def today_tasks():
    print()
    day = datetime.today().day
    month = datetime.today().strftime('%b')
    today = datetime.today().date()
    print(f'Today {day} {month}:')
    Session = sessionmaker(bind=engine)
    session = Session()
    rows = session.query(Task).filter(Task.deadline == today).all()
    if len(rows) == 0:
        print('Nothing to do!')
        print()
    else:
        for i in range(len(rows)):
            print(f'{i+1}. {rows[i].task}')
        print()

def week_tasks():
    print()
    today = datetime.today()
    for i in range(7):
        current = today + timedelta(days=i)
        weekday = current.weekday()
        day = current.day
        month = current.strftime('%b')
        current_date = current.date()
        if weekday == 0:
            weekday = 'Monday'
        elif weekday == 1:
            weekday = 'Tuesday'
        elif weekday == 2:
            weekday = 'Wednesday'
        elif weekday == 3:
            weekday = 'Thursday'
        elif weekday == 4:
            weekday = 'Friday'
        elif weekday == 5:
            weekday = 'Saturday'
        elif weekday == 6:
            weekday = 'Sunday'
        print(f'{weekday} {day} {month}:')
        Session = sessionmaker(bind=engine)
        session = Session()
        rows = session.query(Task).filter(Task.deadline == current_date).all()
        if len(rows) == 0:
            print('Nothing to do!')
            print()
        else:
            for i in range(len(rows)):
                print(f'{i+1}. {rows[i].task}')
            print()

def all_tasks():
    print()
    print('All tasks:')
    Session = sessionmaker(bind=engine)
    session = Session()
    rows = session.query(Task).all()
    if len(rows) == 0:
        print('Nothing to do!')
        print()
    else:
        for i in range(len(rows)):
            current = rows[i].deadline
            day = current.day
            month = current.strftime('%b')
            print(f'{i+1}. {rows[i].task}. {day} {month}')
        print()

def add_task():
    print()
    print('Enter task')
    Session = sessionmaker(bind=engine)
    session = Session()
    task_name = input()
    print('Enter deadline')
    time = datetime.strptime(input(), '%Y-%m-%d')
    new_row = Task(task=task_name,deadline=time)
    session.add(new_row)
    session.commit()
    print('The task has been added!')
    print()

def missed_tasks():
    print()
    print('Missed tasks:')
    Session = sessionmaker(bind=engine)
    session = Session()
    today = datetime.today().date()
    rows = session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()
    if len(rows) == 0:
        print('Nothing is missed!')
        print()
    else:
        for i in range(len(rows)):
            current = rows[i].deadline
            day = current.day
            month = current.strftime('%b')
            print(f'{i+1}. {rows[i].task}. {day} {month}')
        print()

def delete_task():
    print()
    Session = sessionmaker(bind=engine)
    session = Session()
    rows = session.query(Task).order_by(Task.deadline).all()
    if len(rows) == 0:
        print('Nothing to delete!')
        print()
    else:
        print('Chose the number of the task you want to delete:')
        for i in range(len(rows)):
            current = rows[i].deadline
            day = current.day
            month = current.strftime('%b')
            print(f'{i+1}. {rows[i].task}. {day} {month}')
        choosed_delete = int(input())
        delete_row = rows[choosed_delete - 1]
        session.delete(delete_row)
        session.commit()
        print('The task has been deleted!')
        print()

while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    choose = int(input())
    if choose == 1:
        today_tasks()
    elif choose == 2:
        week_tasks()
    elif choose == 3:
        all_tasks()
    elif choose == 4:
        missed_tasks()
    elif choose == 5:
        add_task()
    elif choose == 6:
        delete_task()
    elif choose == 0:
        print()
        print('Bye!')
        break
