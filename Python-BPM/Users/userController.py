from typing import List
import jwt
import bcrypt
from datetime import datetime,timedelta
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.hash import bcrypt
from starlette import status
from starlette.responses import JSONResponse
from Groups.groupModels import GroupIndb
from Users.userModels import *
from config import MONGOURL, MONGODB_NAME, WEBSITE_URL


async def get_users():
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Users")
    allUsers = collection.find({})
    users: List[UserIndb] = []
    async for user in allUsers:
        data = UserIndb(**user)
        users.append(data)
    return users

async def get_users_by_id(id: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Users")
    user = await collection.find_one({'_id': ObjectId(id)})
    if user:
        data = UserIndb(**user)
        return data
    else:
        return {'message': "User Does Not Exist"}

async def get_my_reportees(username: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Users")
    check = await collection.find_one({'username': username})
    reportees: List[UserIndb] = []
    if check:
        users = collection.find({'manager': check['username']})
        async for user in users:
            data = UserIndb(**user)
            reportees.append(data)
        return reportees
    else:
        return {'message': 'User Does Not Exist'}

async def get_my_groups(username: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    rolesCollection = db.get_collection("Roles")
    groupsCollection = db.get_collection("Groups")
    myRoles = rolesCollection.find({'username': username})
    groups: List[GroupIndb] = []
    async for role in myRoles:
        print(role['groupName'])
        group = await groupsCollection.find_one({'groupName': role['groupName']})
        data = GroupIndb(**group)
        groups.append(data)
    return groups

async def post_users(data: User):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Users")
    check = await collection.find_one({'username': data.username})
    if check:
        return {"message": "Already Exists"}
    else:
        newUserData = {
            '_id': None,
            'username': data.username,
            'password': bcrypt.hash(data.password),
            'firstName': data.firstName,
            'lastName': data.lastName,
            'dateOfBirth': data.dateOfBirth,
            'manager': data.manager,
            'role': data.role,
            'aadhar': data.aadhar,
            'pan': data.pan,
            'passport': data.passport,
            'status': data.status,
            'displayPicture': data.displayPicture
        }
        storingNewData = UserIndb(**newUserData)
        await collection.insert_one(storingNewData.dict())
        return {"message": "User Added"}

async def put_user(data: UpdateUser, username: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Users")
    check = await collection.find_one({'username': username})
    if check:
        if bcrypt.verify(data.password, check['password']):
            await collection.update_one({'username': username},
                                        {'$set': {'password': bcrypt.hash(data.password)}})
            return {'message': 'User Modified'}
    else:
        return {'message': 'User Does Not Exist'}

async def delete_users(username: str, password: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Users")
    check = await collection.find_one({"username": username})
    if check:
        data = User(**check)
        if data.password == password and data.username == username:
            await collection.delete_one(data.dict())
            return {"message": "User Deleted"}
        else:
            return {"message": "Please Check The Password"}
    else:
        return {"message": "User Does Not Exists"}

async def login(login: UserLogin):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Users")
    check = await collection.find_one({"username": login.username})
    if check:
        mpassword = check['password']
        print(mpassword)
        if bcrypt.verify(login.password, mpassword):
            token = jwt.encode(
                {'user': login.username, 'scope': 'user', 'iss': WEBSITE_URL,
                 'sub': 'Aryabhatta',
                 'exp': datetime.now() + timedelta(minutes=10)},
                'SECRET_KEY')
            return {'username': login.username,
                    'firstName': check['firstName'],
                    'lastName': check['lastName'],
                    'role': check['role'],
                    'displayPicture': check['displayPicture'],
                    'token': token.decode('UTF-8'),
                    'message': 'Authentication Success'}
        else:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Authentication Failed")
    else:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Authentication Failed")