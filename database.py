import sqlalchemy as sqa
import sqlite3

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db_filename = 'mealcalc.db'

expression = sqa.sql.expression


class Day(Base):
    __tablename__ = 'days'

    id = sqa.Column(sqa.Integer, primary_key=True)

    calories = sqa.Column(sqa.Float)
    protein = sqa.Column(sqa.Float)
    carbs = sqa.Column(sqa.Float)
    fat = sqa.Column(sqa.Float)

    protein_pct = sqa.Column(sqa.Float)
    carbs_pct = sqa.Column(sqa.Float)
    fat_pct = sqa.Column(sqa.Float)

    meal1 = sqa.Column(sqa.String)
    meal2 = sqa.Column(sqa.String)
    meal3 = sqa.Column(sqa.String)
    meal4 = sqa.Column(sqa.String)

    def __repr__(self):
        return ('Day: {} total calories.\n'
                'Macros: {}g protein {}g carb {}g fat.\n'
                'Ratio: {}% protein {}% carb {}% fat.\n'
                '{}'.format(
                    self.calories,
                    self.protein, self.carbs, self.fat,
                    self.protein_pct, self.carbs_pct, self.fat_pct,
                    '\n'.join(
                        [self.meal1, self.meal2, self.meal3, self.meal4]),
                ))


def clear_and_get_sqlite():
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS days')
    c.execute("""
        CREATE TABLE days(
            id INTEGER NOT NULL,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            protein_pct REAL,
            carbs_pct REAL,
            fat_pct REAL,
            meal1 VARCHAR(255),
            meal2 VARCHAR(255),
            meal3 VARCHAR(255),
            meal4 VARCHAR(255),
            PRIMARY KEY(id)
        )
    """)
    conn.commit()
    return conn


def get_orm_session():
    engine = sqa.create_engine('sqlite:///' + db_filename)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
