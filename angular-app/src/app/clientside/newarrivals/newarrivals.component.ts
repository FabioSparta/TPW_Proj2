import { Component, OnInit } from '@angular/core';
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";

@Component({
  selector: 'app-newarrivals',
  templateUrl: './newarrivals.component.html',
  styleUrls: ['./newarrivals.component.css']
})
export class NewarrivalsComponent implements OnInit {
  products : Product[] | undefined;

  constructor(private productService: ProductsService) { }

  ngOnInit(): void {
    this.getNewArrivals();
  }

  getNewArrivals():void{
    this.productService.getNewArrivals().subscribe(products=> this.products = products);
  }

}
