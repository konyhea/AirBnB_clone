#!/usr/bin/python3
''' importing from BaseModel '''
from models.base_model import BaseModel


class City(BaseModel):
    ''' class handling city info '''
    state_id = ""
    name = ""
