import { Component, OnInit } from '@angular/core';
import { UserdataService } from '../services/userdata.service';
import { TaskdataService } from '../services/taskdata.service';
import { Router } from '@angular/router';
import * as Feather from 'feather-icons';
import { GroupdataService } from '../services/groupdata.service';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-userscreen',
  templateUrl: './userscreen.component.html',
  styleUrls: ['./userscreen.component.css']
})
export class UserscreenComponent implements OnInit {

  constructor(private formBuilder: FormBuilder ,private tasks: TaskdataService,private http: HttpClient ,private userdata: UserdataService,private groupdata: GroupdataService,private route: Router) { }
  ngOnInit(): void {
    // this.uploadForm = this.formBuilder.group({
    //   profile: ['']
    // });
    this.getMyTasks();
    this.getMyGroupTasks();
    this.getMyReporteesTasks();
    this.getAllUsers();
    this.getGroups();
    if(this.role=='admin'){
      this.getAllGroups();
    }
  }
  ngAfterViewInit() {
    Feather.replace();
  }
  taskid;taskTitle="";taskDescription;assignedType;assignedTo;
  taskmessage;

  // uploadForm: FormGroup; imageName;
  // onFileSelect(event) {
  //   if (event.target.files.length > 0) {
  //     const file = event.target.files[0];
  //     this.uploadForm.get('profile').setValue(file);
  //   }
  // }

  // onSubmit() {
  //   const formData = new FormData();
  //   formData.append('file', this.uploadForm.get('profile').value);

  //   this.http.post(`http://127.0.0.1:5000/uploadfile`, formData).subscribe(Response=>{
  //     this.imageName= Response['filename']
  //     console.log(this.imageName)
  //   }
  //   );
  // }

  postTaskDetails(){
    console.log(this.taskTitle)
    this.tasks.postTask(this.username,this.taskTitle,this.taskDescription,this.assignedType,this.assignedTo).subscribe(response=>{
      this.taskmessage=response['message'];
    })
  }

  statusChange;taskTitleChange;taskDescriptionChange;currentOwnerChange;updateMessage;comment;
  updateTaskDetails(id: string){
    this.tasks.updateTask(id,this.comment,this.taskTitleChange,this.taskDescriptionChange,this.currentOwnerChange, this.statusChange,this.username).subscribe(response=>{
      this.updateMessage=response['message'];
    })
  }
  username= sessionStorage.getItem("username");
  firstName= sessionStorage.getItem("firstName");
  lastName= sessionStorage.getItem("lastName");
  displayPicture= sessionStorage.getItem("displayPicture");
  role= sessionStorage.getItem("role");

  myTasks;myGroupTasks;myReporteesTasks;
  viewTask;
  getMyTasks(){
    this.tasks.myTasks(this.username).subscribe(Response=>{
      this.myTasks= Response;

    })
  }
  getMyGroupTasks(){
    this.tasks.myGroupTasks(this.username).subscribe(Response=>{
      this.myGroupTasks= Response;
    })
  }
  getMyReporteesTasks(){
    this.tasks.myReporteesTasks(this.username).subscribe(Response=>{
      this.myReporteesTasks= Response;
    })
  }
  getTask(id: string){
    this.tasks.getTaskById(id).subscribe(Response=>{
      this.viewTask=Response;
      this.updateMode=true;
      this.updateMessage="";
      this.taskHistory=null;
      this.taskTitleChange=this.viewTask.taskTitle;
      this.taskDescriptionChange=this.viewTask.taskDescription;
      this.statusChange=this.viewTask.status;
      this.currentOwnerChange= this.viewTask.currentOwner;
      this.comment='';
    })
  }
  signOut(){
    sessionStorage.clear();
    console.log(sessionStorage)
    this.route.navigate(['/login']);
  }
  reloadTasks(){
    this.getMyTasks();
    this.getMyGroupTasks();
    this.getMyReporteesTasks();
  }
  updateMode=true;
  switch_update_mode(){
    if(this.updateMode)
    {
      this.updateMode=false;
    }
    else{
      this.updateMode=true;
    }

  }
  taskHistory;
  taskHistorybyId(id: string)
  {
    this.tasks.getTaskHistory(id).subscribe(Response=>{
      this.taskHistory=Response;
    }
      )
  }
  allusers;
  getAllUsers(){
    this.userdata.getallUsers().subscribe(Response=>{
      this.allusers=Response;
    })
  }
  allGroups;
  getAllGroups(){
    this.groupdata.getallgroups().subscribe(Response=>{
      this.allGroups=Response;
    })
  }
  groups;
  getGroups(){
    this.groupdata.getgroups(this.username).subscribe(Response=>{
      this.groups=Response;
    })
  }
  roles;
  getRolesByGroup(id:string){
    this.groupdata.getroles(id).subscribe(Response=>{
      this.roles=Response;
      console.log(this.roles)
    })
  }
  groupTitle;groupDescription;groupmessage;
  postGroupDetails(){
    this.groupdata.postGroup(this.groupTitle,this.groupDescription).subscribe(Response=>{
      this.groupmessage=Response['message'];
    })
  }
  groupName;roleUser;rolemessage;
  postRoleDetails(){
    this.rolemessage="";
    this.groupdata.postRole(this.groupName,this.roleUser).subscribe(Response=>{
      this.rolemessage=Response['message'];
    })
  }
}
