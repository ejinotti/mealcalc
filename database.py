import sqlalchemy as sqa

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Meal(Base):
    __tablename__ = 'meals'

    id = sqa.Column(sqa.Integer, primary_key=True)
    name = sqa.Column(sqa.String)
    calories = sqa.Column(sqa.Float)
    protein = sqa.Column(sqa.Float)
    carbs = sqa.Column(sqa.Float)
    fat = sqa.Column(sqa.Float)

    daymeals = relationship('DayMeal', back_populates='meal')

    @classmethod
    def from_parts(cls, parts):
        return cls(**cls.combine(parts, with_name=True))

    @classmethod
    def combine(cls, meals, with_name):
        d = {
            'calories': meals[0].calories,
            'protein': meals[0].protein,
            'carbs': meals[0].carbs,
            'fat': meals[0].fat,
        }

        if with_name:
            d['name'] = meals[0].name

        for m in meals[1:]:
            if with_name:
                d['name'] += ' + ' + m.name

            d['calories'] += m.calories
            d['protein'] += m.protein
            d['carbs'] += m.carbs
            d['fat'] += m.fat

        return d

    def __repr__(self):
        return '{}\n{}p {}c {}f {}cal'.format(
            self.name,
            self.protein,
            self.carbs,
            self.fat,
            self.calories,
        )


class DayMeal(Base):
    __tablename__ = 'daymeals'

    id = sqa.Column(sqa.Integer, primary_key=True)
    day_id = sqa.Column(sqa.Integer, sqa.ForeignKey('days.id'))
    meal_id = sqa.Column(sqa.Integer, sqa.ForeignKey('meals.id'))

    day = relationship('Day', back_populates='daymeals')
    meal = relationship('Meal', back_populates='daymeals')

    def __init__(self, meal):
        self.meal = meal


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

    daymeals = relationship('DayMeal', back_populates='day')

    meals = association_proxy('daymeals', 'meal')

    def __init__(self, **kwargs):
        self.calories = kwargs['calories']
        self.protein = kwargs['protein']
        self.carbs = kwargs['carbs']
        self.fat = kwargs['fat']

        self.protein_pct = round(self.protein * 400.0 / self.calories, 1)
        self.carbs_pct = round(self.carbs * 400.0 / self.calories, 1)
        self.fat_pct = round(self.fat * 900.0 / self.calories, 1)

    def __repr__(self):
        return ('Day: {} total calories.\n'
                'Macros: {}g protein {}g carb {}g fat.\n'
                'Ratio: {}% protein {}% carb {}% fat.\n'
                '{}'.format(
                    self.calories,
                    self.protein, self.carbs, self.fat,
                    self.protein_pct, self.carbs_pct, self.fat_pct,
                    '\n'.join([str(m) for m in self.meals]),
                ))


engine = sqa.create_engine('sqlite:///mealcalc.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
