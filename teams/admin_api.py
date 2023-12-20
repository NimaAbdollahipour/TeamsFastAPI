from .models import User, UserRole
from fastapi import APIRouter, status, Depends
from . import session
from .auth2 import pwd_context, get_admin
from teams.schemes import UserScheme

admin_router = APIRouter()


@admin_router.post('/admin/users')
async def create_user(new_user: UserScheme, user: User = Depends(get_admin)):
    user_role = None
    if new_user.role == 'admin':
        user_role = UserRole.ADMIN
    elif new_user.role == 'teacher':
        user_role = UserRole.TEACHER
    else:
        user_role = UserRole.STUDENT
    if session.query(User).count() > 0:
        if session.query(User).filter(User.name == new_user.name).first() or session.query(User).filter(
                User.email == new_user.email).first():
            return {"msg": "User already exists"}, status.HTTP_409_CONFLICT
    new_user_obj = User(
        name=new_user.name,
        email=new_user.email,
        password=pwd_context.hash(new_user.password),
        role=user_role
    )
    session.flush()
    session.add(new_user_obj)
    session.commit()
    return {"msg": "Created User Successfully"}, status.HTTP_201_CREATED


@admin_router.get('/admin/users/{user_id}')
async def get_user(user_id, user: User = Depends(get_admin)):
    ret_user = session.query(User).get(user_id)
    if not ret_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    return {"msg": "Created User Successfully", "user": ret_user}, status.HTTP_200_OK


@admin_router.get('/admin/users')
async def get_all_users(user: User = Depends(get_admin)):
    ret_users = session.query(User).all()
    if not ret_users:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    return {"msg": "Created User Successfully", "users": ret_users}, status.HTTP_200_OK


@admin_router.put('/admin/users/{user_id}')
async def create_user(user_id, updated_user:UserScheme,
                      user: User = Depends(get_admin)):
    ret_user = session.query(User).get(user_id)
    if not ret_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    if updated_user.name:
        ret_user.name = updated_user.name
    if updated_user.email:
        ret_user.name = updated_user.email
    if updated_user.role:
        if updated_user.role == 'admin':
            ret_user.role = UserRole.ADMIN
        elif updated_user.role == 'teacher':
            ret_user.role = UserRole.TEACHER
        else:
            ret_user.role = UserRole.STUDENT
    if updated_user.password:
        ret_user.password = pwd_context.hash(updated_user.password)
    session.commit()
    return {"message": "Updated User Successfully"}, status.HTTP_200_OK


@admin_router.delete('/admin/users/{user_id}')
async def create_user(user_id):
    ret_user = session.query(User).get(user_id)
    if not ret_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    session.delete(ret_user)
    session.commit()
    return {"msg": "Deleted User Successfully", "user": ret_user}, status.HTTP_200_OK
