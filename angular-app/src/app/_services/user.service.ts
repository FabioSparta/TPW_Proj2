import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { REST_API_BASE_URL } from '../GlobalVars';
import { User } from '../_models/user';

const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};


@Injectable({
  providedIn: 'root'
})


export class UserService {
  private baseURL= REST_API_BASE_URL + "/account"

  constructor(private http:HttpClient) { }

  getUserInfo():Observable<any> {
    const url = this.baseURL + "/info"
    return this.http.get<User>(url);
  }

   updateUser(user: {}): Observable<any>  {
    console.log("user right before post")
     console.log(user)
    const url = this.baseURL + '/info/update';
    return this.http.put<any>(url,user , httpOptions);
  }

  newAddress(address: {}): Observable<any>  {
    const url = this.baseURL + '/address/add';
    return this.http.post<any>(url, address, httpOptions);
  }

  updateAddress(address: {}): Observable<any>  {
    const url = this.baseURL + '/address/update';
    return this.http.put<any>(url,address, httpOptions);
  }


}
