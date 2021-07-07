from typing import Dict, List, Tuple, Type, cast
from flask import Blueprint, request

from skywalking import Component
from skywalking.decorators import trace
from skywalking.trace.tags import Tag
from skywalking.trace.span import Span
from skywalking.trace.context import SpanContext, SpanContext, get_context

from . import db
from .models import User


user_bp = Blueprint('user', __name__, url_prefix='/user')
context: SpanContext = get_context()


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



@user_bp.route('', methods=['GET'])
def list_user():
    with context.new_entry_span(op='list user') as span:
        span = cast(Span, span)
        span.component = Component.Flask
        users = db.session.query(User).filter(User.is_deleted == False).all()
        span.log(users)
        return success(users=[user.to_dict(change={'id': 'user_id'}) for user in users])

@trace(op='get user')
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    return success(user=user.to_dict(exclude=['name'], change={'id': 'user_id'}))


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
    params = valid_params(request.json, rules=[('name', str, False), ('is_deleted', bool, False)])
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    if params.get('name')  is not None:
        user.name = params['name']
    if params.get('is_deleted') is not None:
        user.is_deleted = params['is_deleted']
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