import random
import datetime
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import DatabaseError
from models import Base, Group, Teacher, Subject, Student, Grade


def create_data(session):
    try:
        # Ініціалізація Faker
        fake = Faker()

        # Заповнення таблиць
        group_names = ["Group A", "Group B", "Group C"]
        groups = [Group(name=name) for name in group_names]
        session.add_all(groups)

        teacher_names = [fake.name() for _ in range(7)]
        teachers = [Teacher(name=name) for name in teacher_names]
        session.add_all(teachers)

        subject_names = ["Math", "Physics", "Chemistry", "Biology", "History", "Geography", "Literature"]
        subjects = [Subject(name=name, teacher=teachers[i]) for i, name in enumerate(subject_names)]
        session.add_all(subjects)

        students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(20)]
        session.add_all(students)

        for student in students:
            for _ in range(random.randint(10, 20)):
                subject = random.choice(subjects)
                grade = random.uniform(60, 100)
                date = fake.date_between(start_date='-2y', end_date='today')
                session.add(Grade(student=student, subject=subject, grade=grade, date=date))

        # Збереження змін та закриття сесії
        session.commit()
    except DatabaseError as e:
        print.error(e)
        session.rollback()
    finally:
        session.close()