from datetime import datetime

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from pyriver.models.base import BaseModel


class Event(BaseModel):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(Text, default=datetime.utcnow().isoformat)
    timestamp = Column(Text)
    value = Column(Text)
    river = relationship(
        "River",
        lazy="dynamic",
        secondary="river_event_join",
        back_populates="events"
    )
