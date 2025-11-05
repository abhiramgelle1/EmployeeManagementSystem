import { Component, OnInit } from '@angular/core';
import { UserdataService } from '../services/userdata.service';
import { Router } from '@angular/router';
import { DatePipe } from '@angular/common'


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private userdata: UserdataService, private route: Router,public datepipe: DatePipe) { }

  ngOnInit(): void {
     this.changeBG()
  }
  bgs=['space.jpg','work.jpg','data.jpg']
  currentBg;
  i;
  picker;
  startDate = new Date(1990, 0, 1);
  delay() {
    return new Promise(resolve => {
      setTimeout(resolve, 5000);
    });
  }
  async changeBG(){
    while(true)
    {
      for(var bg in this.bgs)
      {
        this.currentBg= this.bgs[bg];
        await this.delay();
      }
    }
  }
  firstname;lastname;username;password;cpassword;date;pan;aadhar;passport;
  token:string="a";
  message;mismatch;
  userLogin(){
    this.userdata.checkLogin(this.username,this.password).subscribe(Response =>{
      this.token = Response['token'];
      console.log(Response)
      sessionStorage.setItem("username",Response['username'])
      sessionStorage.setItem("firstName",Response['firstName'])
      sessionStorage.setItem("lastName",Response['lastName'])
      sessionStorage.setItem("displayPicture",Response['displayPicture'])
      sessionStorage.setItem("role",Response['role'])
      if(this.token.length>0)
      {
        // this.userdata.setLoggedIn();
        // sessionStorage.setItem('')
        this.route.navigate(['/userscreen']);
      }
    },error=>{
      if(error.status>400)
      {
        this.token="";
      }
    })
  }
  postUserDetails(){
    let dateOfBirth =this.datepipe.transform(this.date, 'yyyy-MM-dd');
    if(this.password==this.cpassword){
    this.userdata.postUser(this.username,this.password,this.firstname,this.lastname,dateOfBirth,this.pan,this.aadhar,this.passport,this.photoUrl).subscribe(response =>{
      this.message= response['message'];
    })
  }
  else{
    this.mismatch=true;
  }
  }
  photoUrl;
  onFileSelect(input) {
    console.log(input.files);
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = (e: any) => {
        console.log('Got here: ', e.target.result);
        this.photoUrl = e.target.result;
      }
      reader.readAsDataURL(input.files[0]);
    }
  }

}
