import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

import json

login = input('Type login: ')
password = int(input('Type password: '))
db_name = input('Type name of database: ')

DSN = "f'postgresql://{login}:{password}@localhost:5432/{db_name}'"  # data source name
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


pub1 = Publisher(name='Пушкин')
pub2 = Publisher(name='Гоголь')
pub3 = Publisher(name='Достоевский')
pub4 = Publisher(name='Булгаков')
session.add_all([pub1, pub2, pub3, pub4])
session.commit()

book1 = Book(title='Капитанская дочка', publisher=pub1)
book2 = Book(title='Ревизор', publisher=pub2)
book3 = Book(title='Идиот', publisher=pub3)
book4 = Book(title='Мастер и Маргарита', publisher=pub4)
book5 = Book(title='Евгений Онегин', publisher=pub1)
session.add_all([book1, book2, book3, book4, book5])
session.commit()

sh1 = Shop(name='Буквоед')
sh2 = Shop(name='Читай-город')
sh3 = Shop(name='Лабиринт')
sh4 = Shop(name='Книжный дом')
session.add_all([sh1, sh2, sh3, sh4])
session.commit()

st1 = Stock(book=book1, shop=sh1, count=23)
st2 = Stock(book=book1, shop=sh2, count=54)
st3 = Stock(book=book1, shop=sh3, count=10)
st4 = Stock(book=book2, shop=sh3, count=15)
st5 = Stock(book=book3, shop=sh4, count=24)
st6 = Stock(book=book4, shop=sh2, count=8)
st7 = Stock(book=book5, shop=sh4, count=78)
st8 = Stock(book=book5, shop=sh1, count=3)
session.add_all([st1, st2, st3, st4, st5, st6, st7, st8])
session.commit()

sale1 = Sale(price=829, date_sale='2022-11-11', stock=st3, count=1)
sale2 = Sale(price=402, date_sale='2022-11-10', stock=st7, count=3)
sale3 = Sale(price=790, date_sale='2022-11-10', stock=st6, count=6)
session.add_all([sale1, sale2, sale3])
session.commit()


pub_name = input('Название издательства или фамилия автора: ')
pub_id = input('Идентификатор издательства: ')

def get_publisher(publisher_name=None, publisher_id=None):
    if publisher_id is not None and publisher_name is None:
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale ).\
                join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == pub_id):
            print(f"{c.title}", f"{c.name}", f"{str(c.price * c.count)}", f"{c.date_sale}", sep = ' | ')
    elif publisher_name is not None and publisher_id is None:
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale ).\
                join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name == pub_name):
            print(f"{c.title}", f"{c.name}", f"{str(c.price * c.count)}", f"{c.date_sale}", sep = ' | ')
    elif publisher_name is not None and publisher_id is not None:
        for c in session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale ).\
                join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == pub_id, Publisher.name == pub_name):
            print(f"{c.title}", f"{c.name}", f"{str(c.price * c.count)}", f"{c.date_sale}", sep = ' | ')

if __name__ == '__main__':
    # get_publisher(publisher_name=pub_name)
    # get_publisher(publisher_id=pub_id)
    get_publisher(publisher_id=pub_id, publisher_name=pub_name)

session.close()

