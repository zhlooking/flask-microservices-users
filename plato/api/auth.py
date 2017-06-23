from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc, or_

from plato.api.models import User
from plato import db, bcrypt


auth_blueprint = Blueprint('auth', __name__)


