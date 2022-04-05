from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from poeltl.db.models.base import Base


class Conference(Base):

    __tablename__ = 'conferences'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    divisions = relationship('Division', back_populates='conference')

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r})"
