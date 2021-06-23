from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, Sequence
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from . import db

Base = declarative_base()
metadata = Base.metadata


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(INTEGER(11), primary_key=True)

    def to_dict(self, *, copy: bool=False, change: Dict[str, str]={}, exclude: Sequence[str]=[], extra: Dict[str, Any]={}):
        self.id
        data = deepcopy(self.__dict__) if copy else self.__dict__
        if '_sa_instance_state' in data.keys():
            del data['_sa_instance_state']
        for k, v in data.items():
            if isinstance(v, datetime):
                data[k] = v.timestamp()
            if k in change.keys():
                _k = change[k]
                data[_k] = data[k]
                del data[k]
            if k in exclude:
                del data[k]
        data.update(extra)
        return data


class User(BaseModel):
    __tablename__ = 'user'

    name = Column(String(255), nullable=False)
    create_at = Column(DateTime)
    update_at = Column(DateTime)
    is_deleted = Column(TINYINT(1))