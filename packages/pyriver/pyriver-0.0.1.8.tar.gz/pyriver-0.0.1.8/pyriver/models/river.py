from datetime import datetime

from sqlalchemy import Column, Text, Integer
from sqlalchemy.orm import relationship


from pyriver.models.base import BaseModel


class River(BaseModel):
    __tablename__ = "river"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    create_date = Column(Text, default=datetime.utcnow().isoformat)
    modify_date = Column(Text, default=datetime.utcnow().isoformat)
    name = Column(Text, index=True)
    # user = Column(Text, ForeignKey("user.id"))
    description = Column(Text)
    interval = Column(Text)
    entry = Column(Text)
    schema = Column(Text)
    ochannel = relationship("Channel", uselist=False, back_populates="river")
    events = relationship(
        'Event',
        order_by='desc(Event.timestamp)',
        lazy="dynamic",
        secondary="river_event_join",
        back_populates="river"
    )
    ichannels = relationship(
        "Channel",
        lazy="dynamic",
        secondary="river_channel_join",
        back_populates="subscribers"
    )
