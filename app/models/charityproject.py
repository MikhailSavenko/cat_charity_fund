from sqlalchemy import Column, Text, String
from .base_attr import BaseAttr


class CharityProject(BaseAttr):
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)