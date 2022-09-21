import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres: @localhost:5432/hw_db_6'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def publisher_id_output():
    publisher_id = int(input('Введите id издателя: '))
    query = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == publisher_id)
    for result in query.all():
        print(f'Книги издателя {publisher_id} находятся в магазине {result.name}')


def publisher_name_output():
    publisher_name = input('Введите имя издателя: ')
    query = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher_name)
    for result in query.all():
        print(f'Книги издателя "{publisher_name}" находятся в магазине {result.name}')


if __name__ == '__main__':

    publisher_1 = Publisher(name='Pearson')
    publisher_2 = Publisher(name='Microsoft Press')
    publisher_3 = Publisher(name='No starch press')
    session.add_all([publisher_1, publisher_2, publisher_3])

    shop_1 = Shop(name='Labirint')
    shop_2 = Shop(name='OZON')
    shop_3 = Shop(name='Amazon')
    session.add_all([shop_1, shop_2, shop_3])

    book_1 = Book(title='Modern Operating Systems', publisher=publisher_1)
    book_2 = Book(title='Code Complete: Second Edition', publisher=publisher_2)
    book_3 = Book(title='Hacking: The Art of Exploitation', publisher=publisher_3)
    session.add_all([book_1, book_2, book_3])

    stock_1 = Stock(book=book_1, shop=shop_2, count=40)
    stock_2 = Stock(book=book_2, shop=shop_2, count=50)
    stock_3 = Stock(book=book_3, shop=shop_3, count=10)
    session.add_all([stock_1, stock_2, stock_3])

    sale_1 = Sale(price=10.50, date_sale='2018-10-25T09:52:22.194Z', stock=stock_3, count=9)
    sale_2 = Sale(price=16.00, date_sale='2018-10-25T10:59:56.230Z', stock=stock_2, count=5)
    sale_3 = Sale(price=16.00, date_sale='2018-10-25T10:59:56.230Z', stock=stock_1, count=1)
    session.add_all([sale_1, sale_2, sale_3])

    session.commit()

    publisher_id_output()
    publisher_name_output()

    session.close()
