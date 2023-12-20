from .models import User, Message
from fastapi import APIRouter, Depends, status
from . import session
from datetime import datetime
from .schemes import MessageScheme
from .auth2 import get_current_user

general_router = APIRouter()


@general_router.post('/messages/')
async def send_message(message: MessageScheme, user: User = Depends(get_current_user)):
    receiver = session.query(User).filter(User.name == message.receiver).first()
    if not receiver:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    new_message = Message(
        content=message.content,
        sender_id=user.id,
        receiver_id=receiver.id,
        date_created=datetime.now()
    )
    session.add(new_message)
    session.commit()
    return {"msg": "message sent"}, status.HTTP_201_CREATED


@general_router.get('/messages/{username}/')
async def get_user(username: str, user: User = Depends(get_current_user)):
    other_user = session.query(User).filter(User.name == username).first()
    if not other_user:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    sent_messages = session.query(Message).filter(Message.sender_id == user.id,
                                                  Message.receiver_id == other_user.id).all()
    received_messages = session.query(Message).filter(Message.receiver_id == user.id,
                                                      Message.sender_id == other_user.id).all()
    return {"msg": "retrieved messages successfully", "sent": sent_messages, "received": received_messages}


@general_router.put('/messages/{message_id}/')
async def create_user(message_id: int, content: str, user: User = Depends(get_current_user)):
    message_to_change = session.query(Message).get(message_id)
    if not message_to_change:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    if message_to_change.sender_id != user.id:
        return {"msg": "not allowed to change this message"}, status.HTTP_403_FORBIDDEN
    message_to_change.content = content
    session.commit()
    return {"msg": "updated message successfully", "updated": content}, status.HTTP_200_OK


@general_router.delete('/messages/{message_id}/')
async def create_user(message_id: int, user: User = Depends(get_current_user)):
    message_to_change = session.query(Message).get(message_id)
    if not message_to_change:
        return {"msg": "user not found"}, status.HTTP_404_NOT_FOUND
    if message_to_change.sender_id != user.id:
        return {"msg": "not allowed to delete this message"}, status.HTTP_403_FORBIDDEN
    session.delete(message_to_change)
    session.commit()
    return {"msg": "deleted message successfully"}, status.HTTP_200_OK
