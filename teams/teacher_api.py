from .models import User, UserRole, Team, Channel, Subscription, TeamOwner
from fastapi import APIRouter, status, Depends
from . import session
from .auth2 import get_teacher
from typing import List
from .des_enc import enc

teacher_router = APIRouter()

@teacher_router.post('/teacher/teams')
async def create_team(name: str, user:User = Depends(get_teacher)):
    new_team = Team()
    new_team.creator_id = user.id
    new_team.set_name(name)
    session.add(new_team)
    session.commit()
    return {"msg": "team created successfully"}, status.HTTP_201_CREATED


@teacher_router.get('/teacher/teams')
async def get_teams(user:User = Depends(get_teacher)):
    teams = session.query(Team).filter(Team.creator_id == user.id).all()
    if teams:
        all_teams = [team.get() for team in teams]
        return {"msg": "team retrieved successfully", 'teams':all_teams}, status.HTTP_201_CREATED
    return {"msg": "could not find any team", 'teams':[]}, status.HTTP_404_NOT_FOUND


@teacher_router.delete('/teacher/teams/{team_id}')
async def get_teams(team_id: int, user:User = Depends(get_teacher)):
    team = session.query(Team).get(team_id)
    if team.creator_id!=user.id:
        return {"msg": "user is not the creator of team"}, status.HTTP_401_UNAUTHORIZED
    session.delete(team)
    session.commit()
    return {"msg": "deleted team successfully", 'team':team.get()}, status.HTTP_200_OK


@teacher_router.put('/teacher/teams/{team_id}')
async def get_teams(team_id: int, name: str, user:User = Depends(get_teacher)):
    team = session.query(Team).get(team_id)
    if team.creator_id!=user.id:
        return {"msg": "user is not the creator of team"}, status.HTTP_401_UNAUTHORIZED
    team.set_name(name)
    session.commit()
    return {"msg": "team name updated successfully", 'team':team.get()}, status.HTTP_200_OK


@teacher_router.post('/teacher/teams/{team_id}/member')
async def add_team_members(team_id: int, usernames: List[str], user:User = Depends(get_teacher)):
    team = session.query(Team).get(team_id)
    if team.creator_id!=user.id  and (user not in team.owners):
        return {"msg": "user is not the creator of team"}, status.HTTP_401_UNAUTHORIZED
    encrypted_usernames = [enc(username) for username in usernames]
    for username in encrypted_usernames:
        ret_user = session.query(User).filter(User.name==username).first()
        if ret_user:
            if ret_user.role == UserRole.STUDENT:
                new_sub = Subscription(team_id=team_id, user_id=ret_user.id)
                session.add(new_sub)
    session.commit()
    return {"msg": "team members added successfully (ignored non-student users)"}, status.HTTP_200_OK


@teacher_router.delete('/teacher/teams/{team_id}/member')
async def add_team_members(team_id: int, usernames: List[str], user:User = Depends(get_teacher)):
    team = session.query(Team).get(team_id)
    if team.creator_id!=user.id:
        return {"msg": "user is not the creator of team"}, status.HTTP_401_UNAUTHORIZED
    encrypted_usernames = [enc(username) for username in usernames]
    for username in encrypted_usernames:
        ret_user = session.query(User).filter(User.name==username).first()
        if ret_user:
            sub = session.query(Subscription).filter(Subscription.team_id==team_id, Subscription.user_id==ret_user.id).first()
            if sub:
                session.delete(sub)
    session.commit()
    return {"msg": "team members removed successfully"}, status.HTTP_200_OK


@teacher_router.post('/teacher/teams/{team_id}/owner')
async def add_team_members(team_id: int, usernames: List[str], user:User = Depends(get_teacher)):
    team = session.query(Team).get(team_id)
    if team.creator_id!=user.id:
        return {"msg": "user is not the creator of team"}, status.HTTP_401_UNAUTHORIZED
    encrypted_usernames = [enc(username) for username in usernames]
    for username in encrypted_usernames:
        ret_user = session.query(User).filter(User.name==username).first()
        if ret_user:
            if ret_user.role == UserRole.TEACHER:
                new_sub = TeamOwner(team_id=team_id, user_id=ret_user.id)
                session.add(new_sub)
    session.commit()
    return {"msg": "team owners added successfully (ignored non-teacher users)"}, status.HTTP_200_OK


@teacher_router.delete('/teacher/teams/{team_id}/owner')
async def add_team_members(team_id: int, usernames: List[str], user:User = Depends(get_teacher)):
    team = session.query(Team).get(team_id)
    if team.creator_id!=user.id:
        return {"msg": "user is not the creator of team"}, status.HTTP_401_UNAUTHORIZED
    encrypted_usernames = [enc(username) for username in usernames]
    for username in encrypted_usernames:
        ret_user = session.query(User).filter(User.name==username).first()
        if ret_user:
            sub = session.query(TeamOwner).filter(TeamOwner.team_id==team_id, TeamOwner.user_id==ret_user.id).first()
            if sub:
                session.delete(sub)
    session.commit()
    return {"msg": "team owners removed successfully"}, status.HTTP_200_OK


@teacher_router.post('/teacher/teams/{team_id}/channels')
async def create_channel(team_id: int, name: str, user:User = Depends(get_teacher)):
    team = session.query(Team).get(team_id)
    if not team:
        return {"msg": "team not found"}, status.HTTP_404_NOT_FOUND
    new_channel = Channel()
    new_channel.team_id = team_id
    new_channel.set_name(name)
    team.channels.append(new_channel)
    session.commit()
    return {"msg": "team created successfully"}, status.HTTP_201_CREATED


@teacher_router.get('/teacher/teams/{team_id}/channels/')
async def get_channels(team_id: int, user:User = Depends(get_teacher)):
    channels = session.query(Team).get(team_id).channels
    if channels:
        all_channels = [channel.get() for channel in channels]
        return {"msg": "channels retrieved successfully", 'channels':all_channels}, status.HTTP_200_OK
    return {"msg": "could not find channel", 'channels':[]}, status.HTTP_404_NOT_FOUND


@teacher_router.put('/teacher/channels/{channel_id}')
async def update_channel_name(channel_id: int, name:str, user:User = Depends(get_teacher)):
    channel = session.query(Channel).get(channel_id)
    team = session.query(Team).get(channel.team.get().get('id'))
    if team.creator_id == user.id or user in team.owners:
        channel.set_name(name)
        session.commit()
    return {"msg": "channel name updated"}, status.HTTP_200_OK
