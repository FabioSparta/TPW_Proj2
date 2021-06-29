import { Component, OnInit } from '@angular/core';
import {Category} from "../../_models/category";
import {CategoriesService} from "../../_services/categories.service";

@Component({
  selector: 'app-categories',
  templateUrl: './categories.component.html',
  styleUrls: ['./categories.component.css']
})
export class CategoriesComponent implements OnInit {
  categories : Category[] | undefined;
  constructor(private categoryService : CategoriesService) { }

  ngOnInit(): void {
    this.getCategories();
  }

  getCategories() : void {
    this.categoryService.getCategories().subscribe(categories => this.categories = categories);
  }
}
