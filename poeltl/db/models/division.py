from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Division(Base):

    __tablename__ = 'divisions'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    abbreviation = Column(String(10), nullable=False)
    conference_id = Column(Integer, ForeignKey('conferences.id'), nullable=False)

    conference = relationship('Conference', back_populates='divisions')
    teams = relationship('Team', back_populates='division')

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r}, abbreviation={self.abbreviation!r})"
