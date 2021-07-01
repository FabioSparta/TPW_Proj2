import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {Category} from "../_models/category";

const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class CategoriesService {
  private baseURL= REST_API_BASE_URL + "/categories"

  constructor(private http:HttpClient) { }

  getCategories():Observable<Category[]> {
    return this.http.get<Category[]>(this.baseURL);
  }

}
