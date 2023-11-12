from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Подключение к базе данных MySQL
db_url = "mysql+mysqlconnector://root:Rq237VmT@localhost/samplemysql"  # Замените username и password на ваши учетные данные
engine = create_engine(db_url)

# Создание таблицы
Base = declarative_base()


class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)


# Автоматическое создание таблицы (если она не существует)
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()


def main():
    while True:
        action = input("Что вы хотите сделать? (ввести/считать/выход): ").lower()

        if action == 'ввести':
            name = input("Введите имя: ")
            email = input("Введите адрес электронной почты: ")

            user = UserData(name=name, email=email)
            session.add(user)
            session.commit()

            print("Данные сохранены в базе данных.")
        elif action == 'считать':
            print("Записи в таблице user_data:")
            for user in session.query(UserData).all():
                print(f"ID: {user.id}, Имя: {user.name}, Email: {user.email}, Дата создания: {user.created_at}")
        elif action == 'выход':
            break
        else:
            print("Неправильный выбор. Пожалуйста, введите 'ввести', 'считать' или 'выход'.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
