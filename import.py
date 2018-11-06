import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.exc import DataError
from sqlalchemy.exc import InternalError
from sqlalchemy.exc import IntegrityError

engine = create_engine('postgres://usetpxuboatswg:14291d4b50681090072617602611ea12822484a1e39cde28e9f046fc7ff50a85'
                       '@ec2-54-235-86-226.compute-1.amazonaws.com:5432/d5mk3psi9hs4nb', pool_pre_ping=True)
db = scoped_session(sessionmaker(bind=engine))


if __name__ == '__main__':

    f = open('books.csv')
    reader = csv.reader(f)
    limit = int(input('Limit: '))
    count = 0

    done_tuple = db.execute('SELECT isbn FROM books').fetchall()
    done_list = [book.isbn for book in done_tuple]

    for isbn, title, author, year in reader:

        if count == limit:
            break

        if isbn in done_list:
            continue

        try:
            db.execute('INSERT INTO books(isbn, title, author, year) VALUES(:isbn, :title, :author, :year)',
                       {'isbn': isbn, 'title': title, 'author': author, 'year': year})
            count += 1

        except DataError as e:
            print(str(e))

        except InternalError as e:
            print(str(e))
            break

        except IntegrityError as e:
            print(str(e))
            continue

    db.commit()
    print('Successfully Added {}'.format(count))
