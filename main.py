import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from seed import create_data
from models import create_tables

logging.basicConfig(
    level=logging.INFO,
    format='line_num: %(lineno)s > %(message)s'
)

DBSession = sessionmaker()

def main():
    database = os.getenv('sqlite:///university.db')
    engine = create_engine(
        url=database,
        echo=False
    )
    session = DBSession(bind=engine)

    create_tables(engine)
    logging.info('Tables was generated.')
    create_data(session)
    logging.info('Data was created.')

if __name__ == "__main__":
    main()