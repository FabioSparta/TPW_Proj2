import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../_services/auth.service";
import {Router} from "@angular/router";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Category} from "../../_models/category";
import {CategoriesService} from "../../_services/categories.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isShop: string;
  isAuthenticated : boolean
  username: string;
  categories : Category[] | undefined;
  searchForm: FormGroup;
  searchKey:string;
  searchCat:string;

  constructor(private authService: AuthService,private router: Router,private formBuilder:FormBuilder, private categoriesService:CategoriesService) {
    this.isShop="false";
    this.isAuthenticated=false;
    this.username= "User";
    this.searchKey="";
    this.searchCat="all";
    this.searchForm = formBuilder.group({
        searchVal: ['', Validators.required],
        searchCat: ['all', Validators.required]
      })
  }

  ngOnInit(): void {
    let username = this.authService.getUsername()
    if(username != "") this.username = username;

    let isShop= this.authService.isShop();
    if(isShop!=null) this.isShop= <string>isShop;

    this.isAuthenticated = this.authService.isAuthenticated()
    this.getCategories();
  }

  logout():void{
    this.authService.logout();
    window.location.reload();
  }

  updateKey() {
    this.searchKey=this.searchForm.get('searchVal')?.value;
  }

  updateCat() {
    this.searchCat=this.searchForm.get('searchCat')?.value;
    console.log(this.searchCat);
  }

  getCategories(){
    this.categoriesService.getCategories().subscribe(categories=> {
      this.categories = categories;
    });
  }

  simClick() {
    console.log("entered");
    window.location.replace("/search/"+this.searchKey+"/"+this.searchCat);
  }
}

