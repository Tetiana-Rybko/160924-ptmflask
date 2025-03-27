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
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column,DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float,Boolean
from  dotenv import load_dotenv
from datetime import datetime



Base = declarative_base()

DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///database.db')
engine = create_engine('sqlite:///example.db', echo=True)


class Base(DeclarativeBase):
    pass

sqla_engine = create_engine("sqlite:///example.db", echo=True)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255))


    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=False)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship("Category", back_populates="products")


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()



def main():

    session = Session()


    electronics = Category(name="Электроника", description="Гаджеты и устройства.")
    books = Category(name="Книги", description="Печатные книги и электронные книги.")
    clothing = Category(name="Одежда", description="Одежда для мужчин и женщин.")

    session.add_all([electronics, books, clothing])
    session.commit()


    products = [
        Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
        Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
        Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
        Product(name="Джинсы", price=40.50, in_stock=True, category=clothing),
        Product(name="Футболка", price=20.00, in_stock=True, category=clothing),
    ]

    session.add_all(products)
    session.commit()


    all_categories = session.query(Category).all()
    all_products = session.query(Product).all()

    print("\nКатегории:")
    for c in all_categories:
        print(f"  {c.id}: {c.name} — {c.description}")

    print("\nПродукты:")
    for p in all_products:
        print(f"  {p.id}: {p.name}, Цена: {p.price}, Наличие: {p.in_stock}, Категория: {p.category.name}")

    session.close()

if __name__ == "__main__":
    main()

session.close()