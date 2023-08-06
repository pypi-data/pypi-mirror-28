from sqlalchemy import Table, Column, Integer, ForeignKey

from pyriver.models.base import BaseModel
from pyriver.models import River, Channel    # noqa


river_event_join = Table(
    'river_event_join',
    BaseModel.metadata,
    Column('river_id', Integer, ForeignKey('river.id'), index=True),
    Column('event_id', Integer, ForeignKey('event.id'), index=True),
)

river_channel_join = Table(
    'river_channel_join',
    BaseModel.metadata,
    Column('river_id', Integer, ForeignKey('river.id'), index=True),
    Column('channel_id', Integer, ForeignKey('channel.id'), index=True),
)
