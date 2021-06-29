import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {Product} from "../_models/products";


const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class CategoriesService {
  private baseURL= REST_API_BASE_URL + "/categories"

  constructor(private http:HttpClient) { }

  getCategories():Observable<Product[]> {
    return this.http.get<Product[]>(this.baseURL);
  }

}
