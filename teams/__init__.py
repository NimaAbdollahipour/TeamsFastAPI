from .database import session
from .admin_api import admin_router
from .auth2 import auth_router
from fastapi.middleware.cors import CORSMiddleware
from .general_api import general_router
from .teacher_api import teacher_router
from .student_api import student_router
from .models import (
    PyEnum,
    User,
    Team,
    TeamOwner,
    Subscription,
    Message,
    Announcement,
    Channel)

from fastapi import FastAPI, APIRouter

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(general_router)
app.include_router(teacher_router)
app.include_router(student_router)
