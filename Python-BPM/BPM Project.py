import shutil
from pathlib import Path
import tempfile
from flask import Flask
from flask_pymongo import PyMongo
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn as uvicorn
from starlette.responses import StreamingResponse
from Groups import *
from Users import *
from Roles import *
from Tasks import *

app = FastAPI(title='BPM Portal', description='PROJECT')

flask_app = Flask(__name__)
flask_app.config["MONGO_URI"] = MONGOURL+MONGODB_NAME
mongo = PyMongo(flask_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""GET METHODS"""


@app.get("/users", tags=["Users"])
async def get_users():
    return await userController.get_users()


@app.get("/users/{id}", tags=["Users"])
async def get_users_by_id(id: str):
    return await userController.get_users_by_id(id)


@app.get("/myReportees/{username}", tags=["Users"])
async def get_my_reportees(username: str):
    return await userController.get_my_reportees(username)


@app.get("/myGroups/{username}", tags=["Users"])
async def get_my_groups(username: str):
    return await userController.get_my_groups(username)


@app.get("/groups", tags=["Groups"])
async def get_groups():
    return await groupController.get_groups()


@app.get("/group/{id}", tags=["Groups"])
async def get_group_by_id(id: str):
    return await groupController.get_group_by_id(id)


@app.get("/tasks", tags=["Tasks"])
async def get_tasks():
    return await taskController.get_tasks()

@app.get("/task/{id}", tags=["Tasks"])
async def get_task_by_id(id: str):
    return await taskController.get_task_by_id(id)


@app.get("/myTasks/{username}", tags=["Tasks"])
async def get_my_tasks(username: str):
    return await taskController.get_my_tasks(username)


@app.get("/myGroupTasks/{username}", tags=["Tasks"])
async def get_my_group_tasks(username: str):
    return await taskController.get_my_group_tasks(username)


@app.get("/myReporteesTasks/{username}", tags=["Tasks"])
async def get_my_reportees_tasks(username: str):
    return await taskController.get_my_reportees_tasks(username)

@app.get("/taskHistory/{id}", tags=["Tasks"])
async def get_task_history_by_Id(id: str):
    return await taskController.get_task_history_by_Id(id)


@app.get("/roles", tags=["Roles"])
async def get_roles():
    return await roleController.get_roles()


@app.get("/rolesByGroup/{id}", tags=["Roles"])
async def get_roles_by_group(id: str):
    return await roleController.get_roles_by_group(id)


"""POST METHODS"""

@app.post("/login", tags=["Login"])
async def login(login: UserLogin):
    return await userController.login(login)


@app.post("/users", tags=["Users"])
async def post_users(data: User):
    return await userController.post_users(data)


@app.post("/groups", tags=["Groups"])
async def post_groups(data: Group):
    return await groupController.post_groups(data)


@app.post("/tasks", tags=["Tasks"])
async def post_tasks(data: Task):
    return await taskController.post_tasks(data)


@app.post("/roles", tags=["Roles"])
async def post_roles(role: Role):
    return await roleController.post_roles(role)


"""PUT METHODS"""


@app.put("/user/{username}", tags=["Users"])
async def put_user(data: UpdateUser, username: str):
    return await userController.put_user(data, username)


@app.put("/group/{id}", tags=["Groups"])
async def put_group(id: str, data: GroupIndb):
    return await groupController.put_group(id, data)


@app.put("/task/{id}", tags=["Tasks"])
async def put_task(id: str, comment: str, data: UpdateTask):
    return await taskController.put_task(id, comment, data)


@app.put("/role/{id}", tags=["Roles"])
async def put_role(data: UpdateRole, id: str):
    return await roleController.put_role(data, id)


"""DELETE METHODS"""


@app.delete("/users/{username}/{password}", tags=["Users"])
async def delete_users(username: str, password: str):
    return await userController.delete_users(username, password)


@app.delete("/groups/{id}", tags=["Groups"])
async def delete_group(id: str):
    return await groupController.delete_group(id)


@app.delete("/tasks/{id}", tags=["Tasks"])
async def delete_tasks(id: str):
    return await taskController.delete_tasks(id)

@app.delete("/roles/{id}", tags=["Roles"])
async def delete_role(id: str):
    return await roleController.delete_role(id)

"""METHODS FOR UPLOADING FILES AND GETTING IMAGE"""

@app.post("/getImage/{imageName}", tags=['Files'])
async def get_Image(imageName:str):
    path = Path(tempfile.gettempdir()) / imageName
    file_like = open(path, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpeg")

@app.post("/uploadFile/", tags=['Files'])
async def create_upload_file(file: UploadFile = File(...)):
    print(file.filename)
    contents = await file.read()
    path = Path(tempfile.gettempdir())
    path = path / file.filename
    await save_upload_file(file, path, file.filename)

    return {"filename": file.filename}

async def save_upload_file(upload_file: UploadFile, destination: Path, filename: str) -> None:
    try:

        upload_file.file.seek(0)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            upload_file.file.seek(0)
            mongo.save_file(filename, upload_file.file)
            mongo.db.Files.insert_one(
                {'username': filename, 'file_name': filename})
    finally:
        upload_file.file.close()

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=5000)