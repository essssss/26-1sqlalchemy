from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# Define all our MODELS
class Pet(db.Model):
    """A Pet"""

    __tablename__ = "pets"

    @classmethod
    def get_by_species(cls, species):
        return cls.query.filter_by(species=species).all()

    @classmethod
    def get_all_hungry(cls):
        """return all pets with hunger > 20"""
        return cls.query.filter(Pet.hunger > 20).all()

    def __repr__(self):
        p = self
        return f"<Pet id={p.id} name={p.name} species={p.species} hunger={p.hunger}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), nullable=False, unique=True)

    species = db.Column(db.String(30), nullable=True)

    hunger = db.Column(db.Integer, nullable=False, default=20)

    def greet(self):
        return f"I'm {self.name} the {self.species}"

    def feed(self, amt=20):
        """Update hunger based off of amt"""
        self.hunger -= amt
        self.hunger = max(self.hunger, 0)
