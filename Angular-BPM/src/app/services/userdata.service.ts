import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { toASCII } from 'punycode';


@Injectable({
  providedIn: 'root'
})
export class UserdataService {

  constructor(private http: HttpClient) { }
  apiURL="http://127.0.0.1:5000"
  checkLogin(username: string, password: string){
    return this.http.post(`${this.apiURL}/login`, {
      "username": username,
      "password": password,
    }
    );
  }
  postUser(username: string, password: string, firstName: string, lastName: string, dateOfBirth: string, pan: string, aadhar: string, passport: string, displayPicture: string){
    return this.http.post(`${this.apiURL}/users`, {
      "username": username,
      "password": password,
      "firstName": firstName,
      "lastName": lastName,
      "dateOfBirth": dateOfBirth,
      "status": "active",
      "manager": "none",
      "role": "user",
      "pan": pan,
      "aadhar": aadhar,
      "passport": passport,
      "displayPicture": displayPicture
    }
    );
  }

  getallUsers(){
    return this.http.get(`${this.apiURL}/users`);
  }
  // logInStatus = false;
  // setLoggedIn(){
  //   // this.logInStatus = status;
  //   if(sessionStorage.getItem("username"))
  //   {
  //     return true
  //   }
  // }
  // // getLoggedIn(){

  // // }
}
