import sqlalchemy as sq
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()

class DataBase:
    def __init__(self, login, password, name_db):
        DSN = f'postgresql://{login}:{password}@localhost:5432/{name_db}'
        self.engine = sq.create_engine(DSN)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.session.close()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def searching_author(self):
        publisher_name_id = input("Введите id или имя атора: ")
        sale = self.session.query(Sale).join(Stock).join(Book).join(Publisher
        ).join(Shop).filter(Publisher.name == publisher_name_id).all()
        if sale == []:
            sale = self.session.query(Sale).join(Stock).join(Book
            ).join(Publisher).join(Shop).filter(
            Publisher.id == publisher_name_id).all()
            if sale != []:
                for sale in sale:
                    print(
                    self.session.query(Book).join(Publisher).
                    join(Stock).join(Shop).join(Sale).
                    filter(Sale.id == sale.id).all()[0].title, end=" | "
                    )
                    print(
                        self.session.query(Shop).join(Stock).
                        join(Book).join(Publisher).join(Sale).
                        filter(Sale.id == sale.id).all()[0].name, end=" | "
                        )
                    print(sale.price, end=" | ")
                    print(sale.date_sale)
                return
            else:
                return print('такой кнгиги не продаётся')
        for sale in sale:
            print(
                self.session.query(Book).join(Publisher).
                join(Stock).join(Shop).join(Sale).
                filter(Sale.id == sale.id).all()[0].title, end=" | "
                )
            print(
                self.session.query(Shop).join(Stock).join(Book).
                join(Publisher).join(Sale).filter(Sale.id == sale.id).
                all()[0].name, end=" | "
                )
            print(sale.price, end=" | ")
            print(sale.date_sale)
    
    def load_json_db(self, json_path):
        with open(json_path) as file:
            data = json.load(file)
        for line in data:
            if line["model"] == "publisher":
                publisher = Publisher(id=line["pk"],
                name=line["fields"]["name"])
                self.session.add(publisher)
                self.session.commit()
                self.session.close()
            elif line["model"] == "shop":
                shop = Shop(id=line["pk"],
                name=line["fields"]["name"])
                self.session.add(shop)
                self.session.commit()
                self.session.close()
            elif line["model"] == "book":
                book = Book(id=line["pk"], 
                title=line["fields"]["title"],
                id_publisher=line["fields"]["id_publisher"])
                self.session.add(book)
                self.session.commit()
                self.session.close()
            elif line["model"] == "stock":
                stock = Stock(id=line["pk"], 
                id_shop=line["fields"]["id_shop"],
                id_book=line["fields"]["id_book"],
                count=line["fields"]["count"])
                self.session.add(stock)
                self.session.commit()
                self.session.close()
            elif line["model"] == "sale":
                sale = Sale(id=line["pk"], price=line["fields"]["price"],
                date_sale=line["fields"]["date_sale"],
                count=line["fields"]["count"],
                id_stock=line["fields"]["id_stock"])
                self.session.add(sale)
                self.session.commit()
                self.session.close()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True) 

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'),
     nullable=False)
    relationship(Publisher, backref='book')

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'),
    nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'),
    nullable=False)
    count = sq.Column(sq.Integer)
    relationship(Book, backref='stock')
    relationship(Shop, backref='stock')

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.FLOAT, nullable=False)
    date_sale = sq.Column(sq.TIMESTAMP, server_default=sq.func.now())
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'),
    nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    relationship(Stock, backref='sale')





    


