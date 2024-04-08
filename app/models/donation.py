from sqlalchemy import ForeignKey, Column, Integer, Text
from .base_attr import BaseAttr


class Donation(BaseAttr):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)