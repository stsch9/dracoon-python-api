from .user_responses import RoleList
from .users_models import UserAuthData
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

# required payload for PUT /user/account
class UpdateAccount(BaseModel):
    userName: Optional[str]
    acceptEULA: Optional[bool]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    language: Optional[str]

class UserGroup(BaseModel):
    id: int
    isMember: bool
    name: str

class UserAccount(BaseModel):
    id: int
    userName: str
    firstName: str
    lastName: str
    isLocked: bool
    hasManageableRooms: bool
    userRoles: RoleList
    language: str
    authData: UserAuthData
    mudtSetEmail: Optional[bool]
    needsToAcceptEULA: Optional[bool]
    isEncryptionEnabled: Optional[bool]
    lastLoginSuccessAt: Optional[datetime]
    lastLoginFailAt: Optional[datetime]
    email: Optional[str]
    phone: Optional[str]
    homeRoomId: Optional[int]
    userGroups: Optional[List[UserGroup]]

class UserType(Enum):
    internal = "internal"
    external = "external"
    system = "system"
    deleted = "deleted"

class UserInfo(BaseModel):
    id: int
    userType: UserType
    avatarUuid: str
    userName: str
    firstName: str
    lastName: str
    email: Optional[str]

    
