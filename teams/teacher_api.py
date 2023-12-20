from .models import User, UserRole
from fastapi import APIRouter, status, Depends
from . import session
from .auth2 import get_teacher

teacher_router = APIRouter()


