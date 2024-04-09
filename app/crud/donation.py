from .base import CRUDBase
from models import Donation


class CRUDDonation(CRUDBase):
    pass


danation_crud = CRUDDonation(Donation)