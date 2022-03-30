from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, birth_date={self.birth_date!r}, height_inches={self.height_inches!r}, jersey_number={self.jersey_number!r}, position={self.position!r})"
