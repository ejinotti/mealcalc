import sqlalchemy as sqa

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db_filename = 'mealcalc.db'


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


def create():
    Base.metadata.create_all(engine)


def destroy():
    Base.metadata.drop_all(engine)


engine = sqa.create_engine('sqlite:///{}'.format(db_filename))
create()

Session = sessionmaker(bind=engine)
session = Session()
