from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base


class Player(Base):

    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date)
    height_inches = Column(Integer)
    jersey_number = Column(Integer)
    position = Column(String(10))
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    team = relationship('Team', back_populates='players')

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @hybrid_property
    def height(self):
        if self.height_inches:
            return f"{self.height_inches // 12}\'{self.height_inches % 12}\""

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, age={self.age!r}, height={self.height}, jersey_number={self.jersey_number!r}, position={self.position!r})"
