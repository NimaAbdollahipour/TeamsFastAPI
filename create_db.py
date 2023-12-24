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

teacher2 = User()
teacher2.set_name('jack')
teacher2.set_email('jack@gmail.com')
teacher2.set_password('2001')
teacher2.set_role('teacher')

student2 = User()
student2.set_name('edd')
student2.set_email('edd@gmail.com')
student2.set_password('2001')
student2.set_role('student')

session.add_all((admin, teacher, student, student2, teacher2))
session.commit()
session.close()