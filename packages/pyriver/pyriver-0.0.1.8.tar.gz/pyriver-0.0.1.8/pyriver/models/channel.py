from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from pyriver.models.base import BaseModel


class Channel(BaseModel):
    __tablename__ = "channel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(Text, default=datetime.utcnow().isoformat)
    modify_date = Column(Text, default=datetime.utcnow().isoformat)
    name = Column(Text)
    river_id = Column(Text, ForeignKey("river.id"))
    river = relationship("River", uselist=False, back_populates="ochannel")
    subscribers = relationship(
        "River",
        lazy="dynamic",
        secondary="river_channel_join",
        back_populates="ichannels"
    )

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
