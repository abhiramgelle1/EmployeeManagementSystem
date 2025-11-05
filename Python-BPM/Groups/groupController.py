from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from Groups.groupModels import *
from config import MONGODB_NAME, MONGOURL
import datetime

async def get_groups():
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Groups")
    check = collection.find({})
    groups: List[GroupIndb] = []
    async for group in check:
        data = GroupIndb(**group)
        groups.append(data)
    return groups

async def get_group_by_id(id: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Groups")
    check = await collection.find_one({'_id': ObjectId(id)})
    if check:
        data = GroupIndb(**check)
        return data
    else:
        return {'message': "Group Does Not Exist"}

async def post_groups(data: Group):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Groups")
    check = await collection.find_one({"groupName": data.groupName})
    if check:
        return {"message": "Already Exists"}
    else:
        newGroupData = {
            '_id': None,
            'groupName': data.groupName,
            'description': data.description
        }
        storingNewData = GroupIndb(**newGroupData)
        await collection.insert_one(storingNewData.dict())
        return {"message": "Group Added"}

async def put_group(id: str, data: GroupIndb):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Groups")
    row = await collection.find_one({'_id': ObjectId(id)})
    if row:
        await collection.update_one({'_id': ObjectId(id)},
                                    {'$set': {'groupName': data.groupName,
                                              'description': data.description,
                                              'updatedTime': datetime.datetime.now()}})
        return {'message': 'Group Modified'}
    else:
        return {'message': 'Group Does Not Exist'}

async def delete_group(id: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Groups")
    check = await collection.find_one({"_id": ObjectId(id)})
    if check:
        data = Group(**check)
        await collection.delete_one(data.dict())
        return {"message": "Group Deleted"}
    else:
        return {"message": "Group Does Not Exists"}