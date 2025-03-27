import os
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Identity,
    func
)
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///database.db')
engine = create_engine('sqlite:///example.db', echo=True)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(25))
    age: Mapped[int] = mapped_column(Integer)


    orders: Mapped["Order"] = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    amount: Mapped[float] = mapped_column(Numeric(6, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


    user: Mapped["User"] = relationship("User", back_populates="orders")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


# Пример

user1 = User(name="Лиза", age=15)
user2 = User(name="Кирилл", age=24)


order1 = Order(amount=125.45, user=user1)
order2 = Order(amount=220.50, user=user1)

# Заказ для пользователя Кирилл
order3 = Order(amount=300.00, user=user2)


session.add_all([user1, user2, order1, order2, order3])


session.commit()

orders = session.query(Order).all()
for o in orders:
    print(f"Order {o.id} | User: {o.user.name} | Amount: {o.amount} | Created: {o.created_at}")

session.close()