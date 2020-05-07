from flask import Blueprint
from app.auth import email, forms, routes

bp = Blueprint('auth', __name__)