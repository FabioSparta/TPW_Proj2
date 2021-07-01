import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {Item} from "../_models/items";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";

const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class ItemsService {
  private baseURL= REST_API_BASE_URL + "/items/"

  constructor(private http:HttpClient) { }

  getItems():Observable<Item[]> {
    const url = this.baseURL
    return this.http.get<Item[]>(url);
  }

  getItem(id: number):Observable<Item> {
    const url = this.baseURL + id
    return this.http.get<Item>(url);
  }

  createItem(prod:Item):Observable<any>{
    const url = this.baseURL + "create";
    return this.http.post(url,prod,httpOptions);
  }

  updateItem(prod: Item):Observable<any>{
    const url = this.baseURL + "edit/"+prod.id;
    return this.http.put(url,prod,httpOptions);
  }

  deleteItem(prod: Item):Observable<any>{
    const url = this.baseURL + "delete/"+prod.id;
    return this.http.delete(url,httpOptions);
  }

  itemPerShop(id:number):Observable<Item[]>{
    const url = REST_API_BASE_URL + "/shop/products/"+id;
    return this.http.get<Item[]>(url);
  }
}
