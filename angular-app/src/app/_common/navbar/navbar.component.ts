import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Category} from "../../_models/category";
import {CategoriesService} from "../../_services/categories.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  categories : Category[] | undefined;
  searchForm: FormGroup;
  searchKey:string;
  searchCat:string;

  constructor(private formBuilder:FormBuilder, private categoriesService:CategoriesService) {
  this.searchKey="";
  this.searchCat="all";
  this.searchForm = formBuilder.group({
        searchVal: ['', Validators.required],
        searchCat: ['all', Validators.required]
      })
  }

  ngOnInit(): void {
    this.getCategories();
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

