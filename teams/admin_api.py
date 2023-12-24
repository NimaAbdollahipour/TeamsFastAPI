from .models import User, UserRole, Team, Message, Announcement, Channel
from fastapi import APIRouter, status, Depends
from . import session
from .auth2 import pwd_context, get_admin
from teams.schemes import UserScheme
from .des_enc import des_obj, enc, dec, enc_key
import os
from dotenv import load_dotenv, find_dotenv

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


@admin_router.post('/admin/des/')
async def change_key(key: str, user: User = Depends(get_admin)):
    if len(key)<8:
        return {"msg":"key should be at least 8"}, status.HTTP_400_BAD_REQUEST
    else:
        key = key[:8]
    users = session.query(User).all()
    messages = session.query(Message).all()
    teams = session.query(Team).all()
    channels = session.query(Channel).all()
    anncs = session.query(Announcement).all()

    if users:
        for u in users:
            u.name = enc_key(dec(u.name),key)
            u.email = enc_key(dec(u.email),key)
            u.password = enc_key(dec(u.password),key)
    if messages:
        for m in messages:
            m.content = enc_key(dec(m.content),key)
    if teams:
        for t in teams:
            t.name = enc_key(dec(t.name),key)
    if channels:
        for c in channels:
            c.name = enc_key(dec(c.name),key)
    for a in anncs:
        a.content = enc_key(dec(a.content),key)

    session.commit()

    os.environ['DES_KEY'] = key
    with open(find_dotenv(), 'w') as env_file:
        env_file.write(f'DES_KEY={key}\n')
    return {"msg":"changed key successfully"}, status.HTTP_200_OK