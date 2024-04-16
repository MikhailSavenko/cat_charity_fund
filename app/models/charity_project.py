from sqlalchemy import Column, String, Text

from .base_attr import BaseAttr


class CharityProject(BaseAttr):
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
