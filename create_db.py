from teams.database import engine
from teams.models import Base
from teams.database import session
from teams.models import User, UserRole
from teams.auth2 import pwd_context
from teams.des_enc import des_obj

Base.metadata.create_all(engine)

admin = User()
admin.set_name('peter')
admin.set_email('peter@gmail.com')
admin.set_password('2001')
admin.set_role('admin')

teacher = User()
teacher.set_name('john')
teacher.set_email('john@gmail.com')
teacher.set_password('2001')
teacher.set_role('teacher')

student = User()
student.set_name('sam')
student.set_email('sam@gmail.com')
student.set_password('2001')
student.set_role('student')

session.add_all((admin, teacher, student))
session.commit()
session.close()