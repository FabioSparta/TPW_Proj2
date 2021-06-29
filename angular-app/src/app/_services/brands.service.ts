import { Injectable } from '@angular/core';
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs/internal/Observable";
import {REST_API_BASE_URL} from "../GlobalVars";
import {Brand} from "../clientside/brands/brand";

const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class BrandsService {
  private baseURL= REST_API_BASE_URL + "/brands"

  constructor(private http:HttpClient) { }

  getBrands():Observable<Brand[]> {
    return this.http.get<Brand[]>(this.baseURL);
  }

}
