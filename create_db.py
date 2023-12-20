from teams.database import engine
from teams.models import Base
from teams.database import session
from teams.models import User, UserRole
from teams.auth2 import pwd_context

Base.metadata.create_all(engine)
admin = User(
    name="peter",
    password=pwd_context.hash("2001"),
    role=UserRole.ADMIN,
    email="peter@gmail.com"
)
teacher = User(
    name="john",
    password=pwd_context.hash("1948"),
    role=UserRole.TEACHER,
    email="john@gmail.com"
)
student = User(
    name="edward",
    password=pwd_context.hash("2003"),
    role=UserRole.STUDENT,
    email="edward@gmail.com"
)
session.add_all((admin, teacher, student))
session.commit()
session.close()