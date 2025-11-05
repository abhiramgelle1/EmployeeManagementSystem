from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from Tasks.taskModels import *
from Users.userController import get_my_groups, get_my_reportees
from config import MONGOURL, MONGODB_NAME


async def get_tasks():
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Tasks")
    check = collection.find({})
    tasks: List[TaskIndb] = []
    async for task in check:
        data = TaskIndb(**task)
        tasks.append(data)
    return tasks

async def get_task_by_id(id: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Tasks")
    check = await collection.find_one({'_id': ObjectId(id)})
    if check:
        data = TaskIndb(**check)
        return data
    else:
        return {'message': "Task Does Not Exist"}

async def get_my_tasks(username: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    userCollection = db.get_collection("Users")
    checkUser = await userCollection.find_one({'username': username})
    taskCollection = db.get_collection("Tasks")
    myTasks: List[TaskIndb] = []
    if checkUser:
        verify = taskCollection.find({'currentOwner': checkUser['username']})
        async for task in verify:
            if task['status'] != 'completed' and task['assignedType'] == 'individual':
                data = TaskIndb(**task)
                myTasks.append(data)
        return myTasks
    else:
        return {'message': 'Task Does Not Exist'}

async def get_my_group_tasks(username: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Tasks")
    groups = await get_my_groups(username)
    allTasks = []
    for user in groups:
        group = user.dict()
        taskCollection = collection.find({'currentOwner': group['groupName']})
        async for task in taskCollection:
            groupTasks = TaskIndb(**task)
            allTasks.append(groupTasks)
    return allTasks

async def get_my_reportees_tasks(username: str):
    reportees = await get_my_reportees(username)
    allTasks = []
    for user in reportees:
        reportee = user.dict()
        reporteeTasks = await get_my_tasks(reportee['username'])
        allTasks = allTasks + reporteeTasks
    return allTasks

async def post_tasks(data: Task):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Tasks")
    check = await collection.find_one({"task_title": data.taskTitle})
    if check:
        return {"message": "Already Exists"}
    else:
        newTaskData = {
            '_id': None,
            'taskTitle': data.taskTitle,
            'taskDescription': data.taskDescription,
            'assignedType': data.assignedType,
            'assignedTo': data.assignedTo,
            'createdBy': data.createdBy,
            'currentOwner': data.currentOwner,
            'payload': data.payload,
            'status': data.status,
            'updatedBy': data.updatedBy
        }
        storingNewData = TaskIndb(**newTaskData)
        await collection.insert_one(storingNewData.dict())
        return {"message": "Task Added"}

async def put_task(id: str, comment: str, data: UpdateTask):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    taskCollection = db.get_collection("Tasks")
    taskHistoryCollection = db.get_collection("TaskHistory")
    check = await taskCollection.find_one({'_id': ObjectId(id)})
    if check:
        """To Store All Records In TaskHistory Collection(from line 104-122)"""
        newTaskData = {
            'taskId': id,
            'beforeChanges': {
                'taskTitle': check['taskTitle'],
                'taskDescription': check['taskDescription'],
                'status': check['status'],
                'currentOwner': check['currentOwner']
            },
            'afterChanges': {
                'taskTitle': data.taskTitle,
                'taskDescription': data.taskDescription,
                'status': data.status,
                'currentOwner': data.currentOwner
            },
            'updatedBy': data.updatedBy,
            'comment': comment
        }
        collect = TaskHistory(**newTaskData)
        await taskHistoryCollection.insert_one(collect.dict())
        await taskCollection.update_one({'_id': ObjectId(id)},
                                        {'$set': {'status': data.status,
                                                  'updatedBy': data.updatedBy,
                                                  'taskTitle': data.taskTitle,
                                                  'taskDescription': data.taskDescription,
                                                  'currentOwner': data.currentOwner,
                                                  'updatedTime': datetime.now()}})
        return {'message': 'Task Modified'}
    else:
        return {'message': 'Task Does Not Exist'}

async def delete_tasks(id: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("Tasks")
    check = await collection.find_one({"_id": ObjectId(id)})
    if check:
        data = Task(**check)
        await collection.delete_one(data.dict())
        return {"message": "Task Deleted"}
    else:
        return {"message": "Task Does Not Exists"}

async def get_task_history_by_Id(id: str):
    client = AsyncIOMotorClient(MONGOURL)
    db = client.get_database(MONGODB_NAME)
    collection = db.get_collection("TaskHistory")
    check = collection.aggregate([{'$match': {'taskId': id}}, {'$sort': {'updatedTime': -1}}])
    dataCollection: List[TaskHistory] = []
    if check:
        async for data in check:
            collectingTaskData = TaskHistory(**data)
            dataCollection.append(collectingTaskData)
        return dataCollection
    else:
        return {'message': 'TaskId Does Not Exist'}