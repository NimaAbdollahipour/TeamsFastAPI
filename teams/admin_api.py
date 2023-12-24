from .models import User, UserRole
from fastapi import APIRouter, status, Depends
from . import session
from .auth2 import pwd_context, get_admin
from teams.schemes import UserScheme
from .des_enc import des_obj

admin_router = APIRouter()


@admin_router.post('/admin/users')
async def create_user(new_user: UserScheme, user: User = Depends(get_admin)):
    if session.query(User).count() > 0:
        if session.query(User).filter(User.name == new_user.name).first() or session.query(User).filter(
                User.email == new_user.email).first():
            return {"msg": "User already exists"}, status.HTTP_409_CONFLICT
    new_user_obj = User()
    new_user_obj.set_email(new_user.email)
    new_user_obj.set_role(new_user.role)
    new_user_obj.set_name(new_user.name)
    new_user_obj.set_password(new_user.password)
    session.flush()
    session.add(new_user_obj)
    session.commit()
    return {"msg": "Created User Successfully"}, status.HTTP_201_CREATED


@admin_router.get('/admin/users/{user_id}')
async def get_user(user_id:int, user: User = Depends(get_admin)):
    ret_user = session.query(User).get(user_id)
    if not ret_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    return {"msg": "Retrieved users sucessfully", "user": ret_user.get()}, status.HTTP_200_OK


@admin_router.get('/admin/users')
async def get_all_users(user: User = Depends(get_admin)):
    ret_users = session.query(User).filter(User.name!=user.name).all()
    if not ret_users:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    all_users = [u.get() for u in ret_users]
    return {"msg": "Retrieved users sucessfully", "users": all_users}, status.HTTP_200_OK


@admin_router.put('/admin/users/{user_id}')
async def update_user(user_id:int, updated_user: UserScheme,
                      user: User = Depends(get_admin)):
    ret_user = session.query(User).get(user_id)
    if not ret_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    ret_user.set_name(updated_user.name)
    ret_user.set_email(updated_user.email)
    ret_user.set_role(updated_user.role)
    ret_user.set_password(updated_user.password)
    session.commit()
    return {"message": "Updated User Successfully"}, status.HTTP_200_OK


@admin_router.delete('/admin/users/{user_id}')
async def delete_user(user_id:int, user: User = Depends(get_admin)):
    if user.id == user_id:
        return {"msg": "admin can not delete itself"}, status.HTTP_400_BAD_REQUEST
    ret_user = session.query(User).get(user_id)
    if not ret_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    session.delete(ret_user)
    session.commit()
    return {"msg": "Deleted User Successfully", "user": ret_user}, status.HTTP_200_OK
