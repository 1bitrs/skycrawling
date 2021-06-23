from typing import Dict, List, Tuple, Type
from flask import Blueprint, request
from skywalking.decorators import trace
from . import db
from .models import User


user_bp = Blueprint('user', __name__, url_prefix='/user')


def success(**kwargs):
    return dict(success=True, error_code=0, **kwargs)


def valid_params(params: Dict, *, rules: List[Tuple[str, Type, bool]]):
    new_params: Dict = {}
    for rule in rules:
        if rule[0] in params.keys() and isinstance(params[rule[0]], rule[1]):
            new_params[rule[0]] = params[rule[0]]
        if rule[2] and rule[0] not in params.keys():
            raise Exception(f'param {rule[0]} must be required')
    return new_params

@trace()
@user_bp.route('', methods=['GET'])
def list_user():
    users = db.session.query(User).filter(User.is_deleted == False).all()
    return success(users=[user.to_dict(change={'id': 'user_id'}) for user in users])


@trace()
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    return success(user=user.to_dict(change={'id': 'user_id'}))


@trace()
@user_bp.route('', methods=['POST'])
def add_user():
    params = valid_params(request.json, rules=[('name', str, True), ('is_deleted', bool, False)])
    user = User(**params)
    db.session.add(user)
    db.session.commit()
    return success(user=user.to_dict(change={'id': 'user_id'}))

@trace()
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    params = valid_params(request.json, rules=[('name', str, True)])
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    user.name = params['name']
    db.session.add(user)
    db.session.commit()
    return success(user=user.to_dict(change={'id': 'user_id'}))


@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    user.is_deleted = True
    db.session.add(user)
    db.session.commit()
    return success(user=user.to_dict(change={'id': 'user_id'}))