import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TaskdataService {
  apiURL="http://127.0.0.1:5000"
  constructor(private http: HttpClient) {
    }
    postTask(username:string, taskTitle: string, taskDescription: string,assignedType: string,assignedTo: string){
      return this.http.post(`${this.apiURL}/tasks`, {
        "taskTitle": taskTitle,
        "taskDescription": taskDescription,
        "payload": '-',
        "currentOwner": assignedTo,
        "createdBy": username,
        "assignedType": assignedType,
        "assignedTo": assignedTo,
        "status": "started",
        "updatedBy": username
      }
      );
    }
    updateTask(id:string, comment:string, taskTitle:string, taskDescription:string, currentOwner :string, status: string, updatedBy: string){
      return this.http.put(`${this.apiURL}/task/${id}?comment=${comment}`, {

        "status": status,
        "updatedBy": updatedBy,
        "taskTitle": taskTitle,
        "taskDescription": taskDescription,
        "currentOwner": currentOwner
      }
      );
    }
    getTaskHistory(id:string){
      return this.http.get(`${this.apiURL}/taskHistory/${id}`);
    }
    myTasks(username:string){
      return this.http.get(`${this.apiURL}/myTasks/${username}`)
    }
    myGroupTasks(username:string){
      return this.http.get(`${this.apiURL}/myGroupTasks/${username}`)
    }
    myReporteesTasks(username:string){
      return this.http.get(`${this.apiURL}/myReporteesTasks/${username}`)
    }
    getTaskById(id: string){
      return this.http.get(`${this.apiURL}/task/${id}`)
    }
}
