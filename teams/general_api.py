from .models import User, Message, Chat, Channel, Team, Announcement
from fastapi import APIRouter, Depends, status
from . import session
from datetime import datetime
from .schemes import MessageScheme
from .auth2 import get_current_user
from .des_enc import enc, dec

general_router = APIRouter()


@general_router.post('/messages/')
async def send_message(message: MessageScheme, user: User = Depends(get_current_user)):
    receiver = session.query(User).filter(User.name == enc(message.receiver)).first()
    if not receiver:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    chat = session.query(Chat).filter(
        Chat.users.contains(user) & Chat.users.contains(receiver)
    ).first()
    if not chat:
        chat = Chat(users=[user,receiver])
        session.add(chat)
        session.commit()
    if chat not in user.chats:
        user.chats.append(chat)
    new_message = Message(
        content=enc(message.content),
        chat_id = chat.id,
        receiver_id = receiver.id,
        sender_id = user.id,
        date_created=datetime.now()
    )
    chat.messages.append(new_message)
    session.commit()
    return {"msg": "message sent"}, status.HTTP_201_CREATED


@general_router.get('/messages/chats/{chat_id}/')
async def get_messages(chat_id: int, user: User = Depends(get_current_user)):
    chat = session.query(Chat).get(chat_id)
    if not chat:
        return {"msg": "chat not found"}, status.HTTP_404_NOT_FOUND
    return {"msg": "retrieved messages successfully", "messages":chat.messages}


@general_router.get('/messages/chats/')
async def get_chats(user: User = Depends(get_current_user)):
    chats = user.chats
    if not chats:
        return {"msg": "no chats"}, status.HTTP_404_NOT_FOUND
    chat_names = []
    all_users = []
    for chat in chats:
        all_users.extend(chat.users)
    all_users = set(all_users)
    all_users.remove(user)
    chat_names = [item.get_protected().get('name') for item in all_users]
    return {"msg": "retrieved messages successfully", "chats":chat_names}


@general_router.put('/messages/{message_id}/')
async def update_message(message_id: int, content: str, user: User = Depends(get_current_user)):
    message_to_change = session.query(Message).get(message_id)
    if not message_to_change:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    if message_to_change.sender_id != user.id:
        return {"msg": "not allowed to change this message"}, status.HTTP_403_FORBIDDEN
    message_to_change.content = enc(content)
    session.commit()
    return {"msg": "updated message successfully", "updated": content}, status.HTTP_200_OK


@general_router.delete('/messages/{message_id}/')
async def delete_message(message_id: int, user: User = Depends(get_current_user)):
    message_to_change = session.query(Message).get(message_id)
    if not message_to_change:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    if message_to_change.sender_id != user.id:
        return {"msg": "not allowed to delete this message"}, status.HTTP_403_FORBIDDEN
    session.delete(message_to_change)
    session.commit()
    return {"msg": "deleted message successfully"}, status.HTTP_200_OK


@general_router.get('/users/{user_id}')
async def get_user(user_id:int, user: User = Depends(get_current_user)):
    ret_user = session.query(User).get(user_id)
    if not ret_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    return {"msg": "Retrieved users sucessfully", "user": ret_user.get_protected()}, status.HTTP_200_OK


@general_router.get('/users')
async def get_all_users(user: User = Depends(get_current_user)):
    ret_users = session.query(User).filter(User.name!=user.name).all()
    if not ret_users:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    all_users = [u.get_protected() for u in ret_users]
    return {"msg": "Retrieved users sucessfully", "users": all_users}, status.HTTP_200_OK


@general_router.post('/channels/{channel_id}')
async def send_team_message(channel_id:int, message:str, user:User= Depends(get_current_user)):
    channel = session.query(Channel).get(channel_id)
    if not channel:
        return {"msg": "channel not found"}, status.HTTP_404_NOT_FOUND
    team = session.query(Team).get(channel.team.get().get("id"))
    if user.id == team.creator_id or user in team.owners or user in team.members:
        new_msg = Announcement()
        new_msg.set_content(message)
        new_msg.channel_id = channel.id
        new_msg.user_id = user.id
        new_msg.date_created = datetime.now()
        channel.announcements.append(new_msg)
        session.commit()
        return {"msg": "message sent to channel"}, status.HTTP_201_CREATED
    return {"msg": "you are not allowed to send message to this channel"}, status.HTTP_401_UNAUTHORIZED
    


@general_router.get('/channels/{channel_id}/messages/')
async def get_team_messages(channel_id:int, user:User= Depends(get_current_user)):
    channel = session.query(Channel).get(channel_id)
    if not channel:
        return {"msg": "channel not found"}, status.HTTP_404_NOT_FOUND
    team = session.query(Team).get(channel.team.get().get("id"))
    if user.id == team.creator_id or user in team.owners or user in team.members:
        messages = [message.get() for message in channel.announcements]
        return {"msg": "message sent to channel","messages":messages}, status.HTTP_200_OK
    return {"msg": "you are not allowed to send message to this channel"}, status.HTTP_401_UNAUTHORIZED


@general_router.put('/channels/messages/{message_id}')
async def update_team_message(message_id:int, message:str, user:User= Depends(get_current_user)):
    annc = session.query(Announcement).get(message_id)
    if not annc:
        return {"msg": "message not found"}, status.HTTP_404_NOT_FOUND
    if annc.user_id == user.id:
        annc.set_content(message)
        return {"msg": "message updated successfully","messages":annc.get()}, status.HTTP_200_OK
    return {"msg": "you are not allowed to change message"}, status.HTTP_401_UNAUTHORIZED


@general_router.delete('/channels/messages/{message_id}')
async def delete_team_message(message_id:int, user:User= Depends(get_current_user)):
    annc = session.query(Announcement).get(message_id)
    if not annc:
        return {"msg": "message not found"}, status.HTTP_404_NOT_FOUND
    if annc.user_id == user.id:
        session.delete(annc)
        session.commit()
        return {"msg": "message updated successfully","messages":annc.get()}, status.HTTP_200_OK
    return {"msg": "you are not allowed to change message"}, status.HTTP_401_UNAUTHORIZED