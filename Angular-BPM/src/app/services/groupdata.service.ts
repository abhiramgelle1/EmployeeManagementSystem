import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GroupdataService {

  constructor(private http: HttpClient){ }
  apiURL="http://127.0.0.1:5000"
  getallgroups(){
    return this.http.get(`${this.apiURL}/groups`);
  }
  getgroups(username:string){
    return this.http.get(`${this.apiURL}/myGroups/${username}`);
  }
  getroles(id:string){
    return this.http.get(`${this.apiURL}/rolesByGroup/${id}`)
  }
  postGroup(groupTitle:string, groupDescription:string){
    return this.http.post(`${this.apiURL}/groups`,{
      'groupName': groupTitle,
      'description': groupDescription
    });
  }
  postRole(groupName:string, username:string){
    return this.http.post(`${this.apiURL}/roles`,{
      'groupName': groupName,
      'username': username
    });
  }
}
