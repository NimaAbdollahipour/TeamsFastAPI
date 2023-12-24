from sqlalchemy.orm import relationship, declarative_base
from enum import Enum as PyEnum
from .des_enc import enc,dec
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Sequence,
    Enum,
    Text
)

Base = declarative_base()


class UserRole(PyEnum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_seq', start=1), primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    def set_name(self,name):
        self.name = enc(name)
    def set_email(self,email):
        self.email = enc(email)
    def set_password(self,password):
        self.password = enc(password)
    def set_role(self,role):
        if role == 'admin':
            self.role = UserRole.ADMIN
        elif role == 'teacher':
            self.role = UserRole.TEACHER
        else:
            self.role = UserRole.STUDENT
    def get(self):
        return{
            "id":self.id,
            "name":dec(self.name),
            "email":dec(self.email),
            "password":dec(self.password),
            "role":self.role.value
        }


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, Sequence('annc_seq', start=1), primary_key=True)
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'))
    sender = relationship("User", backref="sent_messages", foreign_keys=[sender_id])
    receiver_id = Column(Integer, ForeignKey('users.id'))
    receiver = relationship("User", backref="received_messages", foreign_keys=[receiver_id])
    date_created = Column(DateTime)

    def set_content(self, content):
        self.content = enc(content)

    def get(self):
        return {
            "id":self.id,
            "sender_id":self.sender_id,
            "receiver_id":self.receiver_id,
            "content":dec(self.content),
            "date_created":self.date_created
        }



class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, Sequence('team_seq', start=1), primary_key=True)
    name = Column(String(64), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", backref="teams")

    def set_name(self, name):
        self.content = enc(name)

    def get(self):
        return {
            "id":self.id,
            "creator_id":self.creator_id,
            "name":dec(self.name),
        }


class TeamOwner(Base):
    __tablename__ = "team_owner"
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
    team = relationship("Team", backref="team_owner", foreign_keys=[team_id])
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User", backref="team_owner", foreign_keys=[user_id])


class Subscription(Base):
    __tablename__ = "subscriptions"
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
    team = relationship("Team", backref="subscriptions", foreign_keys=[team_id])
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User", backref="subscriptions", foreign_keys=[user_id])


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, Sequence('channel_seq', start=1), primary_key=True)
    name = Column(String(64), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", backref="channels")

    def set_name(self, name):
        self.content = enc(name)

    def get(self):
        return {
            "id":self.id,
            "team_id":self.team_id,
            "name":dec(self.name),
        }


class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, Sequence('announcement_seq', start=1), primary_key=True)
    content = Column(Text, nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel = relationship("Channel", backref="announcements", foreign_keys=[channel_id])
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="announcements", foreign_keys=[user_id])
    date_created = Column(DateTime)

    def set_content(self, content):
        self.content = enc(content)

    def get(self):
        return {
            "id":self.id,
            "channel_id":self.channel_id,
            "user_id":self.user_id,
            "content":dec(self.content),
            "date_created":self.date_created
        }


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, Sequence('group_seq', start=1), primary_key=True)
    name = Column(String(64), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", backref="groups")

    def set_name(self, name):
        self.content = enc(name)

    def get(self):
        return {
            "id":self.id,
            "creator_id":self.creator_id,
            "name":dec(self.name),
        }


class GroupMember(Base):
    __tablename__ = 'group_member'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    group = relationship("Group", backref="group_member", foreign_keys=[group_id])
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User", backref="group_member", foreign_keys=[user_id])


class GroupMessage(Base):
    __tablename__ = "group_messages"
    id = Column(Integer, Sequence('group_message_seq', start=1), primary_key=True)
    content = Column(Text, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", backref="group_messages", foreign_keys=[group_id])
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="group_messages", foreign_keys=[user_id])
    date_created = Column(DateTime)

    def set_content(self, content):
        self.content = enc(content)

    def get(self):
        return {
            "id":self.id,
            "group_id":self.group_id,
            "user_id":self.user_id,
            "content":dec(self.content),
            "date_created":self.date_created
        }
