from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from psycopg2 import DatabaseError
from dotenv import load_dotenv
from models import Student, Grade, Subject, Teacher, Group
import sys
import os

# Створення з'єднання з базою даних
engine = create_engine('sqlite:///university.db')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    results = (session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
                      .join(Grade)
                      .group_by(Student.id)
                      .order_by(func.avg(Grade.grade).desc())
                      .limit(5)
                      .all())
    return results

def select_2(subject_id):
    # Знайти студента із найвищим середнім балом з певного предмета
    results = (session.query(Student.name, func.avg(Grade.grade).label('avg_grade'))
                      .join(Grade)
                      .filter(Grade.subject_id == subject_id)
                      .group_by(Student.id)
                      .order_by(func.avg(Grade.grade).desc())
                      .limit(1)
                      .all())
    return results

def select_3(subject_id):
    # Знайти середній бал у групах з певного предмета
    results = (session.query(Group.name, func.avg(Grade.grade).label('avg_grade'))
                      .join(Student)
                      .join(Grade)
                      .filter(Grade.subject_id == subject_id)
                      .group_by(Group.id)
                      .all())
    return results

def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок)
    result = session.query(func.avg(Grade.grade)).scalar()
    return result

def select_5(teacher_id):
    # Знайти які курси читає певний викладач
    results = (session.query(Subject.name)
                      .filter(Subject.teacher_id == teacher_id)
                      .all())
    return results

def select_6(group_id):
    # Знайти список студентів у певній групі
    results = (session.query(Student.name)
                      .filter(Student.group_id == group_id)
                      .all())
    return results

def select_7(group_id, subject_id):
    # Знайти оцінки студентів у окремій групі з певного предмета
    results = (session.query(Student.name, Grade.grade, Grade.date)
                      .join(Grade)
                      .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
                      .all())
    return results

def select_8(teacher_id):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів
    results = (session.query(func.avg(Grade.grade).label('avg_grade'))
                      .join(Subject)
                      .filter(Subject.teacher_id == teacher_id)
                      .scalar())
    return results

def select_9(student_id):
    # Знайти список курсів, які відвідує студент
    results = (session.query(Subject.name)
                      .join(Grade)
                      .filter(Grade.student_id == student_id)
                      .group_by(Subject.id)
                      .all())
    return results

def select_10(student_id, teacher_id):
    # Список курсів, які певному студенту читає певний викладач
    results = (session.query(Subject.name)
                      .join(Grade)
                      .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
                      .group_by(Subject.id)
                      .all())
    return results

def help_command() -> str:

    return "\n'1' - Find 5 students with the highest GPA across all subjects." \
        "\n'2' - Find the student with the highest GPA in a particular subject." \
        "\n'3' - Find the average score in groups for a certain subject." \
        "\n'4' - Find the average score across the entire scoreboard." \
        "\n'5' - Find what courses a particular teacher teaches." \
        "\n'6' - Find a list of students in a specific group." \
        "\n'7' - Find the grades of students in a separate group for " \
            "a specific subject." \
        "\n'8' - Find the avg score given by a certain teacher in his subjects." \
        "\n'9' - Find a list of courses that a particular student is taking." \
        "\n'10' - A list of courses taught to a specific student by a specific teacher."


def main(session) -> None:
    run = True
    print("Hello! I am ready to work.")
    print(help_command())
    while run:
        query = input(
            "\nSelect query option(1 to 10)." \
            "\nEnter 'h' for query list"
            "\nor enter 'q' to exit." \
            "\n --> :").strip().lower()
        match query:
            case "q":
                print("Bye!")
                run = False
                sys.exit(1)
            case "h" | "help":
                print(help_command())
            case "1":
                select_1()
            case "2":
                subject_id = int(input('Enter subject ID: '))
                select_2(subject_id)
            case "3":
                subject_id = int(input('Enter subject ID: '))
                select_3(subject_id)
            case "4":
                select_4()
            case "5":
                teacher_id = int(input('Enter teacher ID: '))
                select_5(teacher_id)
            case "6":
                group_id = int(input('Enter group ID: '))
                select_6(group_id)
            case "7":
                group_id = int(input('Enter group ID: '))
                subject_id = int(input('Enter subject ID: '))
                select_7(group_id, subject_id)
            case "8":
                teacher_id = int(input('Enter teacher ID: '))
                select_8(teacher_id)
            case "9":
                student_id = int(input('Enter student ID: '))
                select_9(student_id)
            case "10":
                student_id = int(input('Enter student ID: '))
                teacher_id = int(input('Enter teacher ID: '))
                select_10(student_id, teacher_id)
            case _:
                print("Wrong input.")
                print(help_command())


if __name__ == '__main__':
    load_dotenv()
    database = os.getenv('sqlite:///university.db')
    engine = create_engine(url=database, echo=False)
    Session = sessionmaker(bind=engine)
    q_session = Session()
    try:
        main(q_session)
    except DatabaseError as e:
        print(e)
    finally:
        q_session.close()