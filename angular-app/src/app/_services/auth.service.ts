import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {BehaviorSubject} from "rxjs";
import {User} from "../_models/user";


const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private userSubject: BehaviorSubject<User>;
  public user: Observable<User> | undefined;

  constructor(private http: HttpClient) {
    this.userSubject = new BehaviorSubject<User>(JSON.parse(<string>localStorage.getItem('user')));
    this.user = this.userSubject.asObservable();
  }

  signUp(user: {}): Observable<any>  {
    alert(user);
    const url = REST_API_BASE_URL + '/account/signup';
    return this.http.post<any>(url, user, httpOptions);
  }

  signIn(username: string, pw: string): Observable < any > {
    const url = REST_API_BASE_URL + '/account/login';
    return this.http.post(url, {username: username, password: pw}, httpOptions);
  }

  logout(): void {
    localStorage.removeItem('userToken');
    localStorage.clear();
  }

  isAuthenticated(): boolean {
    return  localStorage.hasOwnProperty('userToken') && !!localStorage.getItem('userToken');
  }
  getToken(): string {
    return localStorage.getItem('userToken') as string;
  }
}
