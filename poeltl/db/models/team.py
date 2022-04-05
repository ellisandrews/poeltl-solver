from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from poeltl.db.models.base import Base


class Team(Base):

    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    code = Column(String(10), nullable=False)
    division_id = Column(Integer, ForeignKey('divisions.id'), nullable=False)

    division = relationship('Division', back_populates='teams')
    players = relationship('Player', back_populates='team')

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, city={self.city!r}, nickname={self.nickname!r}, code={self.code!r})"
