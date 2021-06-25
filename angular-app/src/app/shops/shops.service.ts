import { Injectable } from '@angular/core';
import {Shop} from "./shop";
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";

@Injectable({
  providedIn: 'root'
})

export class ShopsService {
  private baseURL= REST_API_BASE_URL + "/shops"
  constructor() { }
}

