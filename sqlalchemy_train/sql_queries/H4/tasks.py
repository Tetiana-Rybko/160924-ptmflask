from itertools import product

from sqlalchemy import func
from models_categoty_product import Session,Category,Product


session=Session()

def task2_read_data():
    categories=session.query(Category).all()
    print("Reading data")
    for cat in categories:
        print(f"{cat.name} - {cat.description}")
        if cat.products:
            for prod in cat.products:
                print(f"{prod.name} - {prod.price}")
        else:
            print("No products")
    print("-" * 40)

def task3_update_data():
    smartphone = session.query(Product).filter(Product.name == "Смартфон").first()
    if smartphone:
        print("Updating data")
        print(f"New price 'Смартфон': {smartphone.price}")
        smartphone.price = 329.99
        session.commit()
        #print("New price 'Смартфон': {smartphone.price}")
    else:
        print("No products")
    print("-" * 40)

def task4_aggregation():
    print("Aggregating and Grouping")
    results = session.query(Category.name, func.count(Product.id))\
         .join (Product)\
         .group_by(Category.name)\
         .all()
    for cat_name,prod_count in results:
        print(f"Caterory: {cat_name},Quantity: {prod_count}")
    print("-" * 40)

def task5_grouping_with_filter():
    print("Grouping with filter")
    results = session.query(Category.name, func.count(Product.id).label("product_count")) \
        .join(Product, Category.id == Product.category_id) \
        .group_by(Category.name) \
        .all()
    for cat_name,prod_count in results:
        print(f"Category: {cat_name},Quantity: {prod_count}")
    print("-" * 40)

def main():
        task2_read_data()
        task3_update_data()
        task4_aggregation()
        task5_grouping_with_filter()
        session.close()

if __name__ == "__main__":
    main()
